---
title: _. Start Date vs Logical Date vs Execution Date
tags:
  - airflow
  - python
---

# Airflow start_date 정리
![[Pasted image 20231122025431.png]]
[블로그이미지](https://blog.bsk.im/2021/03/21/apache-airflow-aip-39/)

<div class="notice--success">
start_date 이후의 첫 schedule_interval(aka logical_date)의 실제 실행 시간은 logical_date + schedule_interval 이다
</div>


예시)
*   `start_date` : `2023-04-05 12:00:00` 
*   `schedule_interval` : `(10 * * * *)`
*   `logical_date` : `2023-04-05 12:10:00`
*   `실제 실행시간`: `2023-04-05 13:10:00`
    

# Daily schedule

*   구글에서 찾은 [블로그](https://blog.bsk.im/2021/03/21/apache-airflow-aip-39/)에 의하면 airflow는 time window라는 개념을 이해해야한다고 함. 쇼핑몰을 좋은 예시로 이야기하고 있는데 요약하자면,
*   2023년 5월 3일 쇼핑몰 신규 가입자가 몇 명인지 집계하고자 한다.
	* 신규 가입자 대상: 23년 5월 3일 00~24시 사이에 쇼핑몰에 가입한 이용자
*   상기 조건에 따라 집계하고자 하는 가입자들의 날짜는 5월 3일이지만 취합은 3일 24시를 지난 5월 4일에 진행해야함.
    
<details>
<summary> code 1 </summary>
<div markdown="1">

```py
import os
 from airflow import DAG
 from airflow.operators.dummy import DummyOperator
 from airflow.operators.python import PythonOperator

 from datetime import datetime, timedelta
 import pytz
 import pendulum

 def print_time(**kwargs) -> str:
     time_utc = datetime.now()
     time_kst = time_utc + timedelta(hours=9)
     logical_date = kwargs.get('logical_date')

     print("UTC time: ", time_utc)
     print("KST time: ", time_kst)
     print("context logical_date: ", logical_date)
     print("context logical_date (kst): ", logical_date + timedelta(hours=9))
     return

 kst_timezone = pytz.timezone('Asia/Seoul')

 OWNER = 'rho715@'
 DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")
 DAG_NAME = f'prd01_{DAG_ID}_v1.0.1'
 default_args = {
     'owner': OWNER,
     'dag_id': DAG_ID,
     'depends_on_past': False,
     'start_date': pendulum.datetime(2023, 5, 3, 13, 0, 0,  tz='Asia/Seoul'), #pendulum.now(tz='Asia/Seoul') - timedelta(days=1),
     'email_on_failure': False,
     'email_on_retry': False,
 }

 with DAG(DAG_NAME,
         default_args=default_args,
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         is_paused_upon_creation=True,
         schedule_interval='00 13 * * *',
         tags=['testing']
 ) as dag:
     start = DummyOperator(
         task_id='start',
         dag=dag
     )

     task_01 = PythonOperator(
         task_id='task_01',
         python_callable=print_time,
         provide_context=True,
         execution_timeout=timedelta(minutes=30),
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
<summary> code 2</summary>
<div markdown="1">

```py
import os
 from airflow import DAG
 from airflow.operators.dummy import DummyOperator
 from airflow.operators.python import PythonOperator

 from datetime import datetime, timedelta
 import pytz
 import pendulum

 def print_time(**kwargs) -> str:
     time_utc = datetime.now()
     time_kst = time_utc + timedelta(hours=9)
     logical_date = kwargs.get('logical_date')

     print("UTC time: ", time_utc)
     print("KST time: ", time_kst)
     print("context logical_date: ", logical_date)
     print("context logical_date (kst): ", logical_date + timedelta(hours=9))

     return

 kst_timezone = pytz.timezone('Asia/Seoul')

 OWNER = 'rho715@'
 DAG_ID = os.path.basename(__file__).replace(".pyc", "").replace(".py", "")
 DAG_NAME = f'prd01_{DAG_ID}_v1.0.2'
 default_args = {
     'owner': OWNER,
     'dag_id': DAG_ID,
     'depends_on_past': False,
     'start_date': pendulum.datetime(2023, 5, 3, 17, 0, 0,  tz='Asia/Seoul'), #pendulum.now(tz='Asia/Seoul') - timedelta(days=1),
     'email_on_failure': False,
     'email_on_retry': False,
 }

 with DAG(DAG_NAME,
         default_args=default_args,
         dagrun_timeout=timedelta(hours=2),
         max_active_runs=1,
         max_active_tasks=1,
         catchup=False,
         is_paused_upon_creation=True,
         schedule_interval='00 17 * * *',
         tags=['testing']
 ) as dag:
     start = DummyOperator(
         task_id='start',
         dag=dag
     )

     task_01 = PythonOperator(
         task_id='task_01',
         python_callable=print_time,
         provide_context=True,
         execution_timeout=timedelta(minutes=30),
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

### `code 1`은 실행이 되고 `code 2`는 실행이 안된 이유

*   `code 1`은 `start_date`를 **23년 5월 3일 오후 1시**로 등록 & `schedule_interval`도 **매일 오후 1시**로 설정. 이 뜻은 결국 **23년 5월 3일 오후 1시**의 데이터를 **23년 5월 4일 오후 1시**에 취합 작업을 실행한다는 뜻. 하지만 내가 작업을 **23년 5월 4일 오후 1시 이후**에 등록했으니 *23년 5월 4일 오후 1시*에 돌았어야할 작업이 돌지 않아서 작업을 자동으로 실행해 주었다. ![[Pasted image 20231122025502.png]]

 
*   `code 2`는 `start_date`를 **23년 5월 3일 오후 1시 30분**으로 등록 & `schedule_interval`도 **매일 오후 1시 30분**으로 설정. 따라서 **23년 5월 4일 오후 1시 30분**에 작업이 실행되는데. 내가 작업을 **23년 5월 4일 오후 1시**에 등록했으니 *23년 5월 4일 오후 1시 30분*이 되면 자동으로 실행될 예정이여서 돌지 않았다. ![[Pasted image 20231122025529.png]]

    

# Hourly schedule
## Quiz 1

1.  노윤정이 매시 10분 (`"10 * * * *"`)마다 도는 Airflow DAG를 23년 5월 4일 오후 1시 45분에 배포했을 때 어떻게 될까
    *   `logical_date`은 `2023-05-04 13:10:00` 로 찍히고 자동 실행이 된다
    *   `logical_date`은 `2023-05-04 12:10:00` 로 찍히고 자동 실행이 된다
    *   `logical_date`은 `2023-05-04 13:10:00` 로 찍히지만 자동 실행이 안된다
    *   `logical_date`은 `2023-05-04 12:10:00` 로 찍히지만 자동 실행이 안된다
        
    <details>
    <summary>정답은??</summary>
    <div markdown="1">

    2번
    *   `logical_date`은 `2023-05-04 12:10:00` 데이터가 `2023-05-04 13:10:00` 에 돌았어야해서
    *   `logical_date`은 `2023-05-04 12:10:00` 데이터가 `2023-05-04 13:45:00` 에 실행되었다.

    </div>
    </details> 
            
2.  노윤정이 아래와 같이 배포를 했다. 다음 중 `logical_date`과 `실행시간`이 _**올바르게**_ _**짝지어진**_ 것은?
    
    ```java
    # pendulum.now(tz='Asia/Seoul'): 2023-05-04 13:00:00
    # start_date : pendulum.now(tz='Asia/Seoul') - timedelta(days=1)
    # schedule_interval : (10 * * * *)
    # catchup=False
    ```
    
    1.  `logical_date: 2023-05-03 13:10:00`, `실행시간: 2023-05-03 14:10:00`
    2.  `logical_date: 2023-05-04 13:10:00`, `실행시간: 2023-05-04 14:10:00`
    3.  `logical_date: 2023-05-03 12:10:00`, `실행시간: 2023-05-04 13:00:00`
    4.  `logical_date: 2023-05-04 11:10:00`, `실행시간: 2023-05-04 13:00:00`
    <details>
    <summary>HINT</summary>
    <div markdown="1">

    
    current\_time: `2023-05-04 13:00:00`  ![[Pasted image 20231122032812.png]]

    </div>
    </details>   
    <details>
    <summary>설명</summary>
    <div markdown="1">

    정답: d ![[Pasted image 20231122025630.png]]



    </div>
    </details>   


### 그렇다면 과거 Task 실행안하려면 어떻게 해야하는가 ??
- `- timedelta(days=1)` -> `- timedelta(hours=1)`

current\_time: `2023-05-04 13:00:00`

![[Pasted image 20231122032721.png]]


![[Pasted image 20231122025714.png]]



## Quiz 2

1.  노윤정이 아래와 같이 배포를 하면 어떻게 될지 예상해보자
    
    ```java
    # pendulum.now(tz='Asia/Seoul'): 2023-05-04 13:40:00
    # start_date : pendulum.now(tz='Asia/Seoul') - timedelta(hours=1)
    # schedule_interval : (10 * * * *)
    # catchup=False
    ```
    
    1.  `logical_date은 2023-05-04 13:10:00` 로 찍히고 자동 실행이 된다
    2.  `logical_date은 2023-05-04 12:10:00` 로 찍히고 자동 실행이 된다
    3.  `logical_date은 2023-05-04 13:10:00` 로 찍히지만 자동 실행이 안된다
    4.  `logical_date은 2023-05-04 12:10:00` 로 찍히지만 자동 실행이 안된다 
    <details>
    <summary>HINT</summary>
    <div markdown="1">

    
    current\_time: `2023-05-04 13:40:00` ![[Pasted image 20231122032750.png]]


    </div>
    </details>   
    <details>
    <summary>설명</summary>
    <div markdown="1">

    정답: c ![[Pasted image 20231122025740.png]]


    </div>
    </details>   

# 요약

*   배포 후에 과거 작업이 실행되어도 상관 없다 : `start_date` 하루 전
*   배포 후에 과거 작업이 실행되면 안된다 : `start_date` 한시간 전    
# 참고자료 
- [Airflow DAG start_date 제대로 알기](https://velog.io/@baeyuna97/DAG-startdate)
- [AirflowCatch up, Backfill 알아보기](https://magpienote.tistory.com/236)