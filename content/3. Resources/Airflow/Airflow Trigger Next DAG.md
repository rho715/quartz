---
title: Airflow Trigger Next DAG
tags:
  - airflow
  - python
draft: "false"
---
#### 작업 배경

- GCP Composer로 매 분 데이터를 조회하여 BigQuery로 테이블을 생성하고 있었음
- JSON Data를 BigQuery 테이블을 처음에 Insert 작업을 하다보니 Streaming 조건에 걸려 추후 삭제나 수정이 안되는 이슈로 인해 Python으로 df처리해서 dataframe을 입력하는 방향으로 진행 
- 문제는 이제 통계 DB서버 과부하로 일부 API request가 timeout 혹은 gw지연이 발생하는 경우가 있었는데 
- 기존에는 TASK가 실패하면 슬랙 채널로 알람오는 구조라 어마무시하게 에러가 많이 오게 됨 ![[Screenshot 2023-11-02 at 1.59.52 PM.png]]

- Go lang을 배우면서 Goroutine을 배우고 python도 비슷한 coroutine이 있다하여 API 호출을 병렬적으로 수정하고 데이터 입력하는 TASK에서는 Fail 해도 슬랙 알람을 발생하지 않고 데이터 생성하고 슬랙 알람을 발송하는 슬랙을 Trigger 시켜 서버 복구가 오래 길어지면 데이터 생성은 계속 시도하되 알람은 꺼둘 수 있게 구조를 업데이트 시도
