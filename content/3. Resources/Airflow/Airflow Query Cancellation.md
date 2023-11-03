---
title: Airflow Query Cancellation
tags:
  - bigquery
  - airflow
---


<div class="notice--success">
<h4> 작업 배경  </h4>
<ul> 
    <li> GCP Composer로 매 시간 데이터를 집계하여 테이블을 생성하고 있었음   </li>
    <li> 기본 설정으로 만약 Task가 실패하는 경우 10초뒤에 다시 Task 실행하라고 설정   </li>
    <li> 빅쿼리 슬롯이 모자라 Task 1이 실패하고 retry를 10초뒤에 실행  </li>
    <li> Task가 재실행되는경우 중복 입력 방지를 위해 행상 DELETE query를 실행하는데도 데이터가 중복으로 들어가는 이슈 발견</li>

</ul>
</div>

![[jobs_by_folder.png]]

- 내가 예상한 작업 순서
    - 1 → 2 → 3 → 4 
    - delete → insert → delete → insert

- 실제 작업 순서
    - 1 → 3 → 2 → 4
    - delete → delete → insert → insert

## ?? 왜 첫번째 Task는 실패를 했는데 Query는 성공적으로 실행이 되었을까 ??
<div class="notice--warning">
<h4> 예상 원인  </h4>
<ul> 
    <li> Task가 실패를 하면 query도 캔슬이 되는데 이번에 우연히 캔슬이 되기전에 타이밍 좋게 작업 성공이 되었다.   </li>
    <li> Task가 실패를 해도 query는 캔슬이 안된다.   </li>
</ul>
</div>
![[chatGPT.png]]

- 사실 제발 2번이 아니길.. 하면서 chatGPT한테 물어봤는뎈ㅋㅋ 쿼리는 캔슬이 안된다고 했다...  
- chatGPT를 부정하며 `prd01_dag_retry_delay.py` DAG 파일을 돌려봤다... 
- 아래 이미지처럼 Timeout 이 발생하여 Task는 실패하지만 너무 슬프게도(?) 작업은 성공이 되어있었다.
    - `dag_retry_delay.py` Task 실행 
    - ![[prd01_dag_retry_delay.png]]
    - Task 쿼리 실행 결과   ![[prd01_dag_retry_delay_jbf.png]]

## Task 실패와 동시에 쿼리 캔슬하기 

- 그럼 이제 Task가 실패되어도 쿼리는 취소되지 않는 것을 확인했으니 이제 쿼리 취소하는 부분을 작업에 추가해야겠지.. 
- 해당 코드를 개발하면서 `BigQueryHook`랑 `BigQueryInsertJobOperator` 라이브러리 둘다 `deprecated` 기능이 많아서 진짜 이것저것 시도도 많이 해보고 코드는 돌아가지만 실제로 query 작업이 캔슬이 안되어서 고생을 했는데 결국 그냥 `prd01_dag_retry_delay_cancel.py` 같이 정리했다.
- `job_id`를 생성하고 생성한 `job_id`를 캔슬하는 방식으로 코드를 작성하면서 과연 `query`에 있는 `DELETE & INSERT` 작업 두개 모두 캔슬 되는것인지, 아니면 실행되는 쿼리만 캔슬이 되는지, 아니면 둘다 캔슬이 안되는지 궁금했는데 깔끔하게 실행되고있는 쿼리만 캔슬이 되었다. ![[prd01_dag_retry_delay_cancel_jbf.png]]

## 참고 코드 

<details>
<summary> <code> dag_retry_delay.py </code> </summary>
<div markdown="1">
```python
import os
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
import pytz
import pendulum
from dag_utils.gcp_bigquery_v2 import run_query
import sys

def get_path(_path, step, _dir=None):
    up_path = os.sep.join(_path.split(os.sep)[:-step])
    if _dir is None:
        return up_path
    return os.path.join(up_path, _dir)

module_path = get_path(os.path.dirname(os.path.abspath(__file__)), 2)
sys.path.append(module_path)
KEY_PATH = "data/{key_name}.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=KEY_PATH

def print_time(**kwargs) -> str:
    time_utc = datetime.now()
    time_kst = time_utc + timedelta(hours=9)
    logical_date = kwargs.get('logical_date')

    print("UTC time: ", time_utc)
    print("KST time: ", time_kst)
    print("context logical_date: ", logical_date)
    print("context logical_date (kst): ", logical_date + timedelta(hours=9))

    run_query(owner="local_airflow", query=kwargs['query'])
    return


kst_timezone = pytz.timezone('Asia/Seoul')

OWNER = 'rho715@'
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")
DAG_NAME = f'prd01_{DAG_ID}'
default_args = {
    'owner': OWNER,
    'dag_id': DAG_ID,
    'depends_on_past': False,
    'start_date': pendulum.now(tz='Asia/Seoul') - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
}

query = f"""
# ----------------------------------------------------------------------

DELETE `{target_table}`
WHERE ap_timestamp >= '2023-05-04 00:00:00' and ap_timestamp < '2023-05-04 18:00:00';

# ----------------------------------------------------------------------

INSERT INTO `{target_table}`
SELECT 
  *
FROM `{from}`
WHERE ap_timestamp >= '2023-05-04 00:00:00' and ap_timestamp < '2023-05-04 18:00:00';
"""

with DAG(DAG_NAME,
         default_args=default_args,
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         is_paused_upon_creation=True,
        schedule_interval="10 * * * *",
         tags=['testing']
         ) as dag:
    start = DummyOperator(
        task_id='start',
        dag=dag
    )
    args = {"query":query}
    task_01 = PythonOperator(
        task_id='task_01',
        python_callable=print_time,
        op_kwargs=args,
        provide_context=True,
        execution_timeout=timedelta(seconds=5),
        dag=dag
    )

    end = DummyOperator(
        task_id='end',
        dag=dag
    )

    start >> task_01 >> end
```


</div>
</details>

<details>
<summary> <code> dag_retry_delay_cancel.py </code> </summary>
<div markdown="1">

```python
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.exceptions import AirflowException
import os
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
import pytz
import pendulum
import sys
import uuid

def get_path(_path, step, _dir=None):
    up_path = os.sep.join(_path.split(os.sep)[:-step])
    if _dir is None:
        return up_path
    return os.path.join(up_path, _dir)

module_path = get_path(os.path.dirname(os.path.abspath(__file__)), 2)
sys.path.append(module_path)
KEY_PATH = "data/{key_name}.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=KEY_PATH

kst_timezone = pytz.timezone('Asia/Seoul')
LOC = 'asia-northeast3'

OWNER = 'rho715@'
DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")
DAG_NAME = f'prd01_{DAG_ID}_testing_cancel'
default_args = {
    'owner': OWNER,
    'dag_id': DAG_ID,
    'depends_on_past': False,
    'start_date': pendulum.now(tz='Asia/Seoul') - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
}

query = f"""
# ----------------------------------------------------------------------

DELETE `{target_table}`
WHERE ap_timestamp >= '2023-05-04 00:00:00' and ap_timestamp < '2023-05-04 18:00:00';

# ----------------------------------------------------------------------

INSERT INTO `{target_table}`
SELECT 
  *
FROM `{from}`
WHERE ap_timestamp >= '2023-05-04 00:00:00' and ap_timestamp < '2023-05-04 18:00:00';
"""

def my_bigquery_task(**kwargs):
    time_utc = datetime.now()
    time_kst = time_utc + timedelta(hours=9)
    logical_date = kwargs.get('logical_date')

    print("UTC time: ", time_utc)
    print("KST time: ", time_kst)
    print("context logical_date: ", logical_date)
    print("context logical_date (kst): ", logical_date + timedelta(hours=9))


    job_id = str(uuid.uuid4())
    sql_query = kwargs['query']

    try:
        hook = BigQueryHook()
        hook.insert_job(
            configuration={
                'query': {
                    'query': sql_query,
                    'useLegacySql': False
                }
            },
            job_id=job_id,
            nowait=False
        )

    except Exception as e:

        try:
            from google.cloud import bigquery

            client= bigquery.Client()
            job = client.cancel_job(job_id, location=LOC)
            print(f"{job.location}:{job.job_id} cancelled")
            client.close()

        except AirflowException as ae:
            print("this part is ae") # handle the exception

        raise e

with DAG(DAG_NAME,
         default_args=default_args,
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         is_paused_upon_creation=True,
        schedule_interval="10 * * * *",
         tags=['testing']
         ) as dag:
    start = DummyOperator(
        task_id='start',
        dag=dag
    )
    args = {"query":query}
    task_01 = PythonOperator(
        task_id='task_01',
        python_callable=my_bigquery_task,
        op_kwargs=args,
        provide_context=True,
        execution_timeout=timedelta(seconds=5),
        dag=dag
    )
    end = DummyOperator(
        task_id='end',
        dag=dag
    )

    start >> task_01 >> end

```
</div>
</details>
