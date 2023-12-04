---
title: _. Airflow Trigger Next DAG
tags:
  - airflow
  - python
---
# 작업 배경
- GCP Composer로 매 분 CDN 데이터를 조회하여 BigQuery로 테이블을 생성하고 있었음
- 문제는 이제 통계 DB서버 과부하로 일부 API request가 timeout 혹은 gw지연이 발생하는 경우가 있었는데 
- 기존에는 TASK가 실패하면 슬랙 채널로 알람오는 구조라 어마무시하게 메세지가 많이 오게 됨 ![[Screenshot 2023-11-02 at 1.59.52 PM.png]]
- 하여 코드 리팩토링 작업을 결정

# 수정 포인트
- HTTP request 에러 핸들링
	- 파이썬 배우고 얼마 안되어서 작업한 코드라 retry, exception등 다 처리 안되어있음
- 직렬 -> 병렬
	- Go lang을 배우면서 Goroutine을 배우고 동료가 python도 비슷한 coroutine이 있다하여 API 호출을 병렬처리
- 알람 발송 처리 
	- AS-IS: Task 단위 기준 업무 처리
		- TASK1: API 조회 -> raw 데이터 DF 처리 -> DF BigQuery 입력
		- TASK2: raw JSON 데이터에서 key & value 추출하여 column화 시켜 대시보드용 BigQuery 테이블에 입력
		- Alarm: TASK1 or TASK2 에서 Task failure가 발생하면 슬랙 알림 발송
	- TO-BE: DAG 단위 기준 업무 처리
		- DAG1: API 병렬 조회 -> raw 데이터 DF 처리 -> DF BigQuery입력
		- DAG2: DAG1에서 BigQuery에 입력된 raw JSON 데이터 조회 & key & value 추출하여 column화 시켜 대시보드용 BigQuery에 입력 -> DAG3 Trigger
		- DAG3: DAG2에서 생성된 데이터 조회 & 데이터 없을시 슬랙 알람 발송

> [!note]
> - TASK 단위에서 DAG단위로 변경한이유는 데이터 입력 시도와 별도로 슬랙 알람을 껐다 키기 위함 

# 코드
## 디렉토리 구조
```
{gcs composer bucket}/dags/visual/prd01/
├── 🗂 cdn                  
│ ├── 🐍 visual_cdn_log.py                          : DAG2 
│ ├── 🐍 visual_cdn_raw.py                          : DAG1                       
│ └── 🐍 visual_cdn_slack_condition_alert.py        : DAG3                      
├── 🗂 dag_utils              
│ ├── 🐍 common.py  
│ ├── 🐍 constant.py  
│ ├── 🐍 gcp_bigquery.py
│ ├── 🐍 cdn_api_function.py                        : handle api data
│ ├── 🐍 cdn_table_config.py  
│ └── 🐍 slack_util.py    
└── env.py
```

## API JSON FORMAT
```json
# domain list Response
{
    "reqid": "asdfasdf", // 요청 id
    "reqtime": "2021-04-12 10:00:00",  // 요청 시간
    "rtcode": "200", // 응답 상태 코드
    "data": [ // 권한에 해당하는 도메인 리스트
        "apitest.example.net"
    ],
    "metric": [
        "domain_list"
    ]
}
```

```json
# domain Response
{
    "rtcode": "200", // 응답 상태 코드
    "reqid": "asdfasdf", // 요청 id
    "reqtime": "2021-04-12 10:00:00",  // 요청 시간
    "domain": "apitest.example.net", // 조회 도메인
    "step": "5m", // 조회 단위
    "metric": [ // 데이터 종류 (배열 순서)
        "date",
        "error_ratio"
    ],
    "data": [ // 시간별 데이터 리스트
        [
            1618110000 // Unix Time (int)
            0 //  에러율(float)
        ],
        [
            1618110300,
            0
        ],
        ...
   ]
}
```

## 코드 파일
<details>
<summary> <code> cdn_api_function.py </code> </summary>
<div markdown="1">

```python

import requests  
from requests.exceptions import Timeout, HTTPError  
import time  
import json  
from concurrent.futures import ThreadPoolExecutor, as_completed  
import pandas as pd  
  
# Constants for API URLs and token  
API_URL = 'https://api.example.net/v2/cdn/'  
TOKEN = 'asdfajsldfjasf'  
  
# Common headers  
HEADERS = {  
    'Authorization': f'Token {TOKEN}'  
}  
  
from datetime import datetime  
import pytz  
  
def convert_unix_to_kst(unix_time):  
    kst = pytz.timezone('Asia/Seoul')  
    time_kst = datetime.fromtimestamp(unix_time, kst)  
    return time_kst  
  
  
def get_api_data(session, api_url, headers, params=None, timeout=5, max_retries=3):  
    """Attempts to get data from the API."""  
    retry_delay = 1  # Start with a 1-second delay  
    for attempt in range(max_retries):  
        try:  
            response = session.get(api_url, headers=headers, params=params, timeout=timeout)  
            response.raise_for_status()  
            return response.json()  
        except Timeout:  
            print(f"Request timed out for {api_url}. Retrying in {retry_delay} seconds.")  
            time.sleep(retry_delay)  
            retry_delay *= 2  # Exponential backoff  
        except HTTPError as e:  
            print(f"HTTP error: {e} for {api_url}. No retry.")  
            break  # No retry for HTTP errors other than timeouts  
        except Exception as e:  
            print(f"An error occurred: {e} for {api_url}. No retry.")  
            break  # No retry for other types of errors  
    return None  
  
  
def modify_json(data):  
    """Modifies the JSON data to be more readable."""  
    data_to_transform = data['data'][0]  
    clean_json = dict(zip(data['metric'], data_to_transform))  
    clean_json.pop('date', None)  
    return clean_json  
  
  
def get_domain_data(session, api_url, headers, domain, unix_timestamp):  
    """Retrieves data for a given domain."""  
    params_base = {  
        'date': unix_timestamp,  
        'domain_name': domain,  
        'step': '1m',  
    }  
  
    # Creating a dictionary of API calls we want to make  
    calls = {  
        'traffic': (api_url + 'traffic', params_base),  
        'status': (api_url + 'status', {**params_base, 'show': 'detail'}),  
        'cache': (api_url + 'cache', params_base),  
    }  
  
    results = {}  
  
    # Execute the API calls concurrently  
    with ThreadPoolExecutor() as executor:  
        future_to_api_name = {  
            executor.submit(get_api_data, session, url, headers, params): name for name, (url, params) in calls.items()  
        }  
        for future in as_completed(future_to_api_name):  
            api_name = future_to_api_name[future]  
            try:  
                data = future.result()  
                results[api_name] = modify_json(data)  
            except Exception as e:  
                print(f"{api_name} generated an exception: {e}")  
  
    combined_results = {}  
    for api_name, data in results.items():  
        combined_results.update(data)  
  
    return combined_results  
  
  
def get_data_as_dataframe(unix_timestamp: int):  
    start_time = time.time()  
    """Function that returns data for all domains as a pandas DataFrame."""  
    data_records = []  
  
    # Use a Session object to persist certain parameters across requests  
    with requests.Session() as session:  
        domain_data = get_api_data(session, API_URL + 'domain_list', HEADERS)  
  
        if domain_data and domain_data.get('data'):  
            domains = domain_data['data']  
            with ThreadPoolExecutor() as executor:  
                # Submit all domain data retrieval jobs to the executor  
                futures = {executor.submit(get_domain_data, session, API_URL, HEADERS, domain, unix_timestamp): domain  
                           for domain in domains}  
  
                # As each job completes, process the results  
                for future in as_completed(futures):  
                    domain = futures[future]  
                    try:  
                        combined_results = future.result()  
                        # Append a record for each domain  
                        data_records.append({  
                            'unix_timestamp': unix_timestamp,  
                            'domain_name': domain,  
                            'data': json.dumps(combined_results)  
                        })  
                    except Exception as e:  
                        print(f"An error occurred for domain {domain}: {e}")  
  
    end_time = time.time()  
    print(f"Total time: {end_time - start_time} seconds")  
  
    # Convert the list of records into a DataFrame  
    df = pd.DataFrame(data_records)  
    return df

```
</div>
</details>
<details>
<summary> <code> visual_cdn_raw.py </code> </summary>
<div markdown="1">

```python
  
#############################  LIBRARIES  
import os  
from datetime import datetime, timedelta  
import json  
  
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator  
from airflow.models import Variable  
  
from visual.prd01 import env  
from visual.prd01.dag_utils.slack_cloudfn import SlackAlert  
from visual.prd01.dag_utils import common  
from visual.prd01.dag_utils.gcp_bigquery import save_to_bq, run_query  
from visual.prd01.dag_utils.skbcdn_api_function import convert_unix_to_kst, get_data_as_dataframe  
from visual.prd01.dag_utils.skbcdn_table_config import {company}_raw_media_traffic_skbcdn  
  
SLACK_INFO = Variable.get(env.airflow_alert_key, None)  
SLACK_INFO = json.loads(SLACK_INFO)  
alert = SlackAlert(channel=SLACK_INFO.get('channel'), slack_info=SLACK_INFO)  
  
LOC = 'asia-northeast3'  
default_args = {  
    'owner': 'rho715@{company}.com',  
    'depends_on_past': False,  
    'email_on_failure': False,  
    'email_on_retry': False,  
    # 'on_failure_callback': alert.slack_fail_alert  
}  
  
from visual.prd01.dag_utils.{company}_cdn_media_traffic import MediaTrafficSKB  
  
############################# BQ 설정 부분  
project_id = common.get_current_project_id()  
  
############################# BQ 설정 부분 - {company}_raw.media_traffic_skbcdndestination_skbcdn = f"{project_id}.{company}_raw.media_traffic_skbcdn"  
job_config_skbcdn = {company}_raw_media_traffic_skbcdn  
  
  
############################# 데이터 호출 부분  
def set_time(**kwargs):  
  
    # time_utc = datetime.now() - timedelta(minutes=5)  
    time_utc = kwargs.get('logical_date') - timedelta(minutes=5)  
    time_without_seconds = time_utc.replace(second=0, microsecond=0)  
    unix_time = int(time_without_seconds.timestamp())  
  
    unix_time_kst = convert_unix_to_kst(unix_time)  
  
    print("Processing Time (UTC): ", time_without_seconds)  
    print("Processing Time (KST): ", unix_time_kst)  
    print("unix_time: ", unix_time)  
  
    return_time = {  
        'unix_time': unix_time,  
        'unix_time_kst': unix_time_kst  
    }  
    return return_time  
  
  
def process_media_traffic_{company}_raw(**kwargs):  
    owner = default_args['owner']  
  
    return_time = kwargs.get('ti').xcom_pull(task_ids=['set_unix_time'])  
    return_time = return_time[0]  
    unix_time, unix_time_kst = (return_time.get('unix_time'), return_time.get('unix_time_kst'))  
  
    df = get_data_as_dataframe(unix_time)  
  
    query = f"""  
    DELETE `{project_id}.{company}_raw.media_traffic_skbcdn`  
    WHERE ap_timestamp = '{unix_time_kst}'  
    """  
    run_query(owner, query)  
  
    # save dataframe  
    kwargs_df = {'dataframe': df, 'destination': kwargs['destination'], 'job_config': kwargs['job_config']}  
    save_to_bq(**kwargs_df)  
  
    return_time = {  
        'str_s_time': str(unix_time_kst),  
        'str_e_time': str(unix_time_kst + timedelta(minutes=1))  
    }  
    return return_time  
  
  
# ############################################################################################################################## DAGS : haystack #####  
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  
with DAG(  
    dag_id=f'{env.prefix}_{DAG_ID}_v1.0.0',  
    default_args=default_args,  
    schedule_interval='10 * * * *',  
    start_date=datetime(2023, 11, 3, 0, 0, 0),  
    max_active_runs=3,  
    catchup=True,  
    is_paused_upon_creation=True,  
    tags=['api', 'skbcdn', '{company}_raw'],  
) as dag:  
    set_unix_time = PythonOperator(  
        task_id='set_unix_time',  
        provide_context=True,  
        python_callable=set_time,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=10)  
    )  
    prd_{company}_raw_skbcdn = PythonOperator(  
        task_id='prd_{company}_raw_skbcdn_insert',  
        provide_context=True,  
        op_kwargs=default_args,  
        python_callable=process_media_traffic_{company}_raw,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=30)  
    )  
    set_unix_time >> prd_{company}_raw_skbcdn

```
</div>
</details>
<details>
<summary> <code> visual_cdn_log.py </code> </summary>
<div markdown="1">

```python
  
#############################  LIBRARIES  
import os  
from datetime import datetime, timedelta  
import json  
  
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator  
from airflow.models import Variable  
from airflow.models import DagModel  
from airflow.operators.trigger_dagrun import TriggerDagRunOperator  
  
from visual.prd01 import env  
from visual.prd01.dag_utils.slack_cloudfn import SlackAlert  
from visual.prd01.dag_utils import common  
from visual.prd01.dag_utils.gcp_bigquery import run_query  
from visual.prd01.dag_utils.skbcdn_table_config import {company}_log_media_traffic_skbcdn  
  
SLACK_INFO = Variable.get(env.airflow_alert_key, None)  
SLACK_INFO = json.loads(SLACK_INFO)  
alert = SlackAlert(channel=SLACK_INFO.get('channel'), slack_info=SLACK_INFO)  
  
LOC = 'asia-northeast3'  
default_args = {  
    'owner': 'rho715@{company}.com',  
    'depends_on_past': False,  
    'email_on_failure': False,  
    'email_on_retry': False,  
    # 'on_failure_callback': alert.slack_fail_alert  
}  
  
  
############################# BQ 설정 부분  
project_id = common.get_current_project_id()  
DATE_FORMAT = '%Y-%m-%dT%H:%M:00Z'  
  
############################# 데이터 호출 부분  
def set_time(**kwargs):  
  
    # time_utc = datetime.now() - timedelta(minutes=5)  
    time_utc = kwargs.get('logical_date') - timedelta(minutes=8)  
  
    str_s_time = common.get_arg(kwargs, 'str_s_time')  # KST  
    if not str_s_time:  
        str_s_time = time_utc + timedelta(hours=9)  
        str_s_time = str_s_time.strftime(DATE_FORMAT)  
  
    str_e_time = common.get_arg(kwargs, 'str_e_time')  # KST  
    if not str_e_time:  
        str_e_time = time_utc + timedelta(hours=9)  
        str_e_time = str_e_time.strftime(DATE_FORMAT)  
  
    print(" ===== START TIME :: " + str_s_time)  
    print(" ===== END TIME   :: " + str_e_time)  
  
    return_time = {  
        'str_s_time': str_s_time,  
        'str_e_time': str_e_time  
    }  
    return return_time  
  
  
def process_media_traffic_{company}_log(**kwargs):  
    owner = default_args['owner']  
  
    return_time = kwargs.get('ti').xcom_pull(task_ids=['set_unix_time'])  
    return_time = return_time[0]  
    str_s_time, str_e_time = (return_time.get('str_s_time'), return_time.get('str_e_time'))  
  
    start_time = datetime.strptime(str_s_time, DATE_FORMAT)  
    end_time = datetime.strptime(str_e_time, DATE_FORMAT)  
  
    while start_time < end_time:  
        yyyy_mm_dd = start_time.strftime('%Y-%m-%d')  
        yyyymmdd = yyyy_mm_dd.replace('-', '')  
  
        start_time_loop = start_time #2022-08-05 00:00:00  
        delta_minutes = timedelta(minutes=1)  
        end_time_loop = start_time_loop + delta_minutes #2022-08-05 01:00:00  
  
        query = {company}_log_media_traffic_skbcdn.format(  
        project_id=project_id,  
        yyyymmdd=yyyymmdd,  
        start_time_loop=start_time_loop,  
        end_time_loop=end_time_loop,  
    )  
        run_query(owner, query)  
  
        start_time = end_time_loop  
  
def is_dag_paused(dag_id):  
    dag_model = DagModel.get_current(dag_id)  
    return dag_model.is_paused  
  
def run_trigger(**kwargs):  
    return_time = kwargs.get('ti').xcom_pull(task_ids=['set_unix_time'])  
    return_time = return_time[0]  
    str_s_time, str_e_time = (return_time.get('str_s_time'), return_time.get('str_e_time'))  
  
    trigger_args = {'str_s_time': str_s_time, 'str_e_time': str_e_time}  
  
    trigger_version = "v1.0.0"  
    target_dag_name = f'{env.prefix}_visual_skbcdn_slack_condition_alert_{trigger_version}'  
  
    # is_dag_paused : True 이면 dag off, False 이면 dag on    if is_dag_paused(target_dag_name):  
        print(f"{target_dag_name} - DAG OFF")  
    else:  
        print(f"{target_dag_name} - trigger start")  
        print(f"trigger_args : {trigger_args}")  
        trigger_next_dag = TriggerDagRunOperator(  
            trigger_dag_id=f'{target_dag_name}',  
            task_id='trigger_next_dag',  
            conf=trigger_args  
        )  
        trigger_next_dag.execute(kwargs)  
  
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  
with DAG(  
    dag_id=f'{env.prefix}_{DAG_ID}_v1.0.0',  
    default_args=default_args,  
    schedule_interval='10 * * * *',  
    start_date=datetime(2023, 11, 3, 0, 0, 0),  
    max_active_runs=3,  
    catchup=True,  
    is_paused_upon_creation=True,  
    tags=['api', 'skbcdn', '{company}_log'],  
) as dag:  
    set_unix_time = PythonOperator(  
        task_id='set_unix_time',  
        provide_context=True,  
        python_callable=set_time,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=10)  
    )  
    prd_{company}_log_skbcdn = PythonOperator(  
        task_id='prd_{company}_log_skbcdn_insert',  
        provide_context=True,  
        op_kwargs=default_args,  
        python_callable=process_media_traffic_{company}_log,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=30)  
    )  
    task_trigger = PythonOperator(  
        task_id='trigger_skbcdn_monitoring',  
        provide_context=True,  
        op_kwargs=default_args,  
        python_callable=run_trigger,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=10)  
    )  
    set_unix_time >> prd_{company}_log_skbcdn >> task_trigger

```
</div>
</details>
<details>
<summary> <code> visual_cdn_slack_condition_alert.py </code> </summary>
<div markdown="1">

```python

#############################  LIBRARIES  
import os  
from datetime import datetime, timedelta  
  
from airflow import DAG  
from airflow.operators.python_operator import PythonOperator  
  
from visual.prd01 import env  
from visual.prd01.dag_utils.constant import DEFAULT_SLACK  
from visual.prd01.dag_utils.slack_util import SlackUtil  
from visual.prd01.dag_utils.gcp_bigquery import run_query_df  
  
  
alert = SlackUtil(DEFAULT_SLACK.get('channel'))  
  
LOC = 'asia-northeast3'  
default_args = {  
    'owner': 'rho715@{company}.com',  
    'depends_on_past': False,  
    'email_on_failure': False,  
    'email_on_retry': False,  
    'on_failure_callback': alert.send_alert_message  
}  
  
  
def get_args(context):  
    str_s_time = context['dag_run'].conf.get('str_s_time')  
    str_e_time = context['dag_run'].conf.get('str_e_time')  
    return str_s_time, str_e_time  
  
def run_job(**kwargs):  
    str_s_time, str_e_time = get_args(kwargs)  
    owner = default_args['owner']  
    data_check_query = """  
    """.format(str_s_time, str_e_time)  
    df = run_query_df(owner, data_check_query)  
  
    if df:  
        print(df)  
    else:  
        msg = f"No Data Found for : {str_s_time} ~ {str_e_time}"  
        kwargs['task_instance'].xcom_push(key='message', value=msg)  
        alert.send_alert_message(kwargs)  
  
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  
with DAG(  
    dag_id=f'{env.prefix}_{DAG_ID}_v1.0.0',  
    default_args=default_args,  
    schedule_interval=None,  
    start_date=datetime(2021, 8, 1, 0, 0, 0),  
    catchup=False,  
    is_paused_upon_creation=True,  
    tags=['api', '{company}_raw', '{company}_log'],  
) as dag:  
    skbcdn_slack_alert = PythonOperator(  
        task_id='skbcdn_slack_alert',  
        provide_context=True,  
        python_callable=run_job,  
        dag=dag,  
        execution_timeout=timedelta(minutes=15),  
        retries=3,  
        retry_delay=timedelta(seconds=10)  
    )  
  
    skbcdn_slack_alert

```
</div>
</details>

# 작업 log
- 왜 데이터 프레임 처리를 하였는가
	- 처음에 JSON Data를 하나하나 BigQuery 테이블로 Insert 작업을 하다보니 Streaming 조건에 걸려 추후 삭제나 수정이 안되는 이슈로 데이터 재생성에 어려움을 겪음
	- 따라서 Python으로 df처리해서 dataframe을 입력하는 방향으로 진행 