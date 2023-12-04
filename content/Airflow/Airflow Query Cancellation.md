---
title: _. Airflow Query Cancellation
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
    - `dag_retry_delay.py` Task 실행 ![[prd01_dag_retry_delay.png]]
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
	WHERE ap_timestamp between '2023-05-04 00:00:00'  and 
	and '2023-05-04 18:00:00';
	
	# ----------------------------------------------------------------------

	INSERT INTO `{target_table}`
	SELECT 
	  *
	FROM `{from}`
	WHERE ap_timestamp between '2023-05-04 00:00:00'  and 
	and '2023-05-04 18:00:00';
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
		WHERE ap_timestamp between '2023-05-04 00:00:00'  and 
		and '2023-05-04 18:00:00';
	
	# ----------------------------------------------------------------------
	
	INSERT INTO `{target_table}`
	SELECT 
	  *
	FROM `{from}`
		WHERE ap_timestamp between '2023-05-04 00:00:00'  and 
		and '2023-05-04 18:00:00';
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

## 최신 버전 
<details>
<summary> <code> load_notes.py </code> </summary>
<div markdown="1">

```python
	
	#############################  LIBRARIES  
	import os  
	from datetime import datetime, timedelta  
	import json  
	import uuid  
	import logging  
	from google.cloud import bigquery, storage  
	  
	from airflow import DAG  
	from airflow.operators.python_operator import PythonOperator  
	from airflow.models import Variable  
	  
	from load.prd01 import env  
	from load.prd01.dag_utils.slack_cloudfn import SlackAlert  
	from load.prd01.dag_utils import common  
	from load.prd01.dag_utils.gcp_bigquery import run_query_df, run_query, delete_gcs_backup_files, get_gcs_backup_files  
	  
	SLACK_INFO = Variable.get(env.airflow_alert_key, None)  
	SLACK_INFO = json.loads(SLACK_INFO)  
	alert = SlackAlert(channel=SLACK_INFO.get('channel'), slack_info=SLACK_INFO)  
	  
	LOC = 'asia-northeast3'  
	default_args = {  
	    'owner': 'rho715@company.com',  
	    'depends_on_past': False,  
	    'email_on_failure': False,  
	    'email_on_retry': False,  
	    'on_failure_callback': alert.slack_fail_alert  
	}  
	  
	# common #####  
	warehouse_project = Variable.get('warehouse_project') #for backup  
	project_id = common.get_current_project_id()  
	dataset = 'company_log'  
	  
	path_sql_files = env.cur_dir + '/dag_utils/sql_files/'  
	DATE_FORMAT = '%Y-%m-%d %H:00:00'  
	  
	# functions #####  
	  
	def run_query_with_cancellation(query, job_id):  
	    bq_client = bigquery.Client()  
	    try:  
	        print(f"THIS IS RUNNING ID: {job_id}")  
	        bq_job = bq_client.query(query, job_id=job_id)  
	        bq_job.result()  
	    except Exception as e:  
	        try:  
	            print(f"CANCELING ID: {job_id}")  
	            bq_job = bq_client.get_job(job_id=job_id, location=LOC)  
	            bq_job.cancel()  
	        except Exception as cancel_error:  
	            logging.error("Failed to cancel job:", cancel_error)  
	        raise e  
	  
	def run_backup_py(**kwargs):  
	    """backup to GCS before run_py()"""  
	    bup_dataset = kwargs['bup_dataset']  
	    table_name = kwargs['table_name']  
	  
	    path_query_backup = f"{path_sql_files}backup.{bup_dataset}"+'.sql' # -> utils/sql_files/backup.haystack.sql  
	    with open(path_query_backup) as f:  
	        query_format = f.read() \  
	        .replace('{warehouse_project}', warehouse_project) \  
	        .replace('{project}', project_id) \  
	        .replace('{dataset}', bup_dataset) \  
	        .replace('{datatable}', table_name)  
	  
	    exe_dt = kwargs.get('logical_date') # UTC Datetime  
	  
	    str_s_time = common.get_arg(kwargs, 'str_s_time')  # KST  
	    if not str_s_time:  
	        str_s_time = exe_dt + timedelta(hours=9)  
	        str_s_time = str_s_time.strftime(DATE_FORMAT)  
	  
	    str_e_time = common.get_arg(kwargs, 'str_e_time')  # KST  
	    if not str_e_time:  
	        str_e_time = exe_dt + timedelta(hours=10)  
	        str_e_time = str_e_time.strftime(DATE_FORMAT)  
	  
	    print(" ===== START TIME :: " + str_s_time)  
	    print(" ===== END TIME   :: " + str_e_time)  
	  
	    start_time = datetime.strptime(str_s_time, DATE_FORMAT)  
	    end_time = datetime.strptime(str_e_time, DATE_FORMAT)  
	  
	    while start_time < end_time:  
	        yyyy_mm_dd = start_time.strftime('%Y-%m-%d')  
	        yyyymmdd = yyyy_mm_dd.replace('-', '')  
	        yyyy, mm, dd = (yyyymmdd[:4], yyyymmdd[4:6], yyyymmdd[6:])  
	        hh = start_time.strftime('%H')  
	  
	        # when task retried, delete existing files  
	        delete_gcs_backup_files(warehouse_project, bup_dataset, table_name, yyyymmdd, hh)  
	  
	        start_time_loop = '{start_time} {hh}:00:00'.format(start_time=yyyy_mm_dd, hh=hh) #2022-08-05 00:00:00  
	        delta_hour = timedelta(hours=1)  
	        end_time_loop = datetime.strptime(start_time_loop, DATE_FORMAT) + delta_hour #2022-08-05 01:00:00  
	  
	        query = query_format.format(yyyymmdd=yyyymmdd  
	                                    , yyyy=yyyy  
	                                    , mm=mm, dd=dd, hh=hh  
	                                    , start_time=start_time_loop, end_time=end_time_loop)  
	  
	        job_id = 'rho715_backup_haystack_{uid}'.format(uid=uuid.uuid1())  
	        logging.info(f"exec query:\n{query}")  
	  
	        run_query_with_cancellation(query, job_id)  
	  
	        gcs_output = get_gcs_backup_files(warehouse_project, bup_dataset, table_name, yyyymmdd, hh)  
	        if len(gcs_output) == 0:  
	            raise Exception("*** No backed up files ***")  
	  
	        start_time = end_time_loop  
	  
	    return_time = {  
	        'str_s_time': str_s_time,  
	        'str_e_time': str_e_time  
	    }  
	    return return_time  
	  
	def run_create_py(**kwargs):  
	    """create sharded table"""  
	    owner = default_args['owner']  
	    table_name = kwargs['table_name']  
	  
	    path_query_table_info = f"{path_sql_files}"+'company_meta.table_info.sql' # GCS SQL FILE DIRECTIORY  
	    with open(path_query_table_info) as f:  
	        query = f.read().replace('{project}', project_id).replace('{dataset}', dataset)  
	    DF_table_info = run_query_df(owner, query)  
	    query_format = DF_table_info[DF_table_info['table_name'].str.startswith(table_name+'_{yyyymmdd}')]['ddl_create_if_not_exists'].item()  
	  
	    return_time = kwargs.get('ti').xcom_pull(task_ids=['prd_haystack_backup'])  
	    return_time = return_time[0]  
	    str_s_time, str_e_time = (return_time.get('str_s_time'), return_time.get('str_e_time'))  
	  
	    print(" ===== START TIME :: " + str_s_time)  
	    print(" ===== END TIME   :: " + str_e_time)  
	  
	    start_time = datetime.strptime(str_s_time, DATE_FORMAT)  
	    end_time = datetime.strptime(str_e_time, DATE_FORMAT)  
	  
	    while start_time < end_time:  
	        yyyy_mm_dd = start_time.strftime('%Y-%m-%d')  
	        yyyymmdd = yyyy_mm_dd.replace('-', '')  
	        hh = start_time.strftime('%H')  
	  
	        start_time_loop = '{start_time} {hh}:00:00'.format(start_time=yyyy_mm_dd, hh=hh) #2022-08-05 00:00:00  
	        delta_hour = timedelta(hours=1)  
	        end_time_loop = datetime.strptime(start_time_loop, DATE_FORMAT) + delta_hour #2022-08-05 01:00:00  
	        query = query_format.format(yyyymmdd=yyyymmdd)  
	  
	        run_query(owner, query)  
	  
	        start_time = end_time_loop  
	#  
	def run_insert_py(**kwargs):  
	    table_name = kwargs['table_name']  
	  
	    path_query = f"{path_sql_files}companydp-prd.{dataset}.{table_name}"+'.sql'  
	    with open(path_query) as f:  
	        query_format = f.read().replace('companydp-prd', project_id)  
	  
	    return_time = kwargs.get('ti').xcom_pull(task_ids=['prd_haystack_backup'])  
	    return_time = return_time[0]  
	    str_s_time, str_e_time = (return_time.get('str_s_time'), return_time.get('str_e_time'))  
	  
	    print(" ===== START TIME :: " + str_s_time)  
	    print(" ===== END TIME   :: " + str_e_time)  
	  
	    start_time = datetime.strptime(str_s_time, DATE_FORMAT)  
	    end_time = datetime.strptime(str_e_time, DATE_FORMAT)  
	  
	    while start_time < end_time:  
	        yyyy_mm_dd = start_time.strftime('%Y-%m-%d')  
	        yyyymmdd = yyyy_mm_dd.replace('-', '')  
	        hh = start_time.strftime('%H')  
	  
	        start_time_loop = '{start_time} {hh}:00:00'.format(start_time=yyyy_mm_dd, hh=hh) #2022-08-05 00:00:00  
	        delta_hour = timedelta(hours=1)  
	        end_time_loop = datetime.strptime(start_time_loop, DATE_FORMAT) + delta_hour #2022-08-05 01:00:00  
	  
	        query = query_format.format(yyyymmdd=yyyymmdd, start_time=start_time_loop, end_time=end_time_loop)  
	  
	        job_id = 'rho715_insert_{uid}'.format(uid=uuid.uuid1())  
	        logging.info(f"exec query:\n{query}")  
	  
	        run_query_with_cancellation(query, job_id)  
	  
	        start_time = end_time_loop  
	  
	  
	# ############################################################################################################################## DAGS : haystack #####  
	DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")  
	with DAG(  
	    dag_id=f'{env.prefix}_{DAG_ID}_v1.1.1',  
	    default_args=default_args,  
	    schedule_interval='10 * * * *',  
	    start_date=datetime(2021, 7, 1),  
	    max_active_runs=1,  
	    catchup=False,  
	    is_paused_upon_creation=True,  
	    tags=['haystack', dataset],  
	) as dag:  
	    prd_haystack_backup_args = {'bup_dataset': 'haystack', 'table_name': 'notes'}  
	    prd_haystack_backup = PythonOperator(  
	        task_id='prd_haystack_backup',  
	        provide_context=True,  
	        op_kwargs=prd_haystack_backup_args,  
	        python_callable=run_backup_py,  
	        dag=dag,  
	        execution_timeout=timedelta(minutes=15),  
	        retries=3,  
	        retry_delay=timedelta(seconds=10)  
	    )  
	    # ############################################################################################################################## DAGS : notes #####  
	    prd_notes_create_args = {'table_name': 'notes'}  
	    prd_notes_create = PythonOperator(  
	        task_id='prd_notes_create',  
	        provide_context=True,  
	        op_kwargs=prd_notes_create_args,  
	        python_callable=run_create_py,  
	        dag=dag,  
	        execution_timeout=timedelta(minutes=15),  
	        retries=3,  
	        retry_delay=timedelta(seconds=10)  
	    )  
	  
	    prd_notes_insert_args = {'table_name': 'notes'}  
	    prd_notes_insert = PythonOperator(  
	        task_id='prd_notes_insert',  
	        provide_context=True,  
	        op_kwargs=prd_notes_insert_args,  
	        python_callable=run_insert_py,  
	        dag=dag,  
	        execution_timeout=timedelta(minutes=15),  
	        retries=3,  
	        retry_delay=timedelta(minutes=5)  
	    )  
	    #  
	    # ############################################################################################################################## DAGS : notes_hourly #####    prd_notes_hourly_create_args = {'table_name': 'notes_hourly'}  
	    prd_notes_hourly_create = PythonOperator(  
	        task_id='prd_notes_hourly_create',  
	        provide_context=True,  
	        op_kwargs=prd_notes_hourly_create_args,  
	        python_callable=run_create_py,  
	        dag=dag,  
	        execution_timeout=timedelta(minutes=15),  
	        retries=3,  
	        retry_delay=timedelta(seconds=10)  
	    )  
	  
	    prd_notes_hourly_insert_args = {'table_name': 'notes_hourly'}  
	    prd_notes_hourly_insert = PythonOperator(  
	        task_id='prd_notes_hourly_insert',  
	        provide_context=True,  
	        op_kwargs=prd_notes_hourly_insert_args,  
	        python_callable=run_insert_py,  
	        dag=dag,  
	        execution_timeout=timedelta(minutes=15),  
	        retries=3,  
	        retry_delay=timedelta(minutes=5)  
	    )  
	  
	    # ############################################################################################################################## run #####  
	    prd_haystack_backup >> prd_notes_create >> prd_notes_insert >> prd_notes_hourly_create >> prd_notes_hourly_insert
```
</div>
</details>