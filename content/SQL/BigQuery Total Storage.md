---
title: . BigQuery Total Storage
tags:
  - bigquery
---

# 목적/배경
- 현재 프로젝트에서 사용하고 있는 빅쿼리 저장소 크기를 파악하기 위함

# 조회 방법 

1. chatGPT가 알려준 방법 : [metrics explorer 사용](https://cloud.google.com/monitoring/charts/metrics-explorer?hl=ko)
	   ![[2023-03-17-chatGPT.png]]
	   ![[2023-03-17-metrics explorer.png]]

2. [TABLE_STORAGE_BY_ORGANIZATION](https://cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization?hl=ko)

# 조회시 주의사항?
- 작성일 기준 (2023-03-31) TABLE_STORAGE_BY_ORGANIZATION 기능은 프리뷰 버전으로 사용상에 제약이 있을 수 있다고 공유 받음 
- metrics explorer vs TABLE_STORAGE_BY_ORGANIZATION 
	- 대체적으로 비슷 
- logical vs physical
	- logical: 데이터 세트의 기본 청구 모델 & 논리적인 바이트. 개별 열의 데이터 유형을 기반으로 계산 된다. 
        - 예. INT64는 8개의 논리 바이트 사용
        -  physical: 실질적으로 디스크에 저장되는 용량. 타임스탬프가 포함되며 물리 디스크에 압축되어 저장되는 사이즈 (default 7days)
        - 요약: BigQuery Table의 추가가 1일 5회씩 1개의 row 추가될 경우 Logical Bytes는 row추가에 따른 테이블 사이즈가 증가. 하지만 Physical Bytes는 데이터가 변경될시의 [Table 전체 사이즈+타임스탬프]가 압축되어 총 5회 저장. 따라서 데이터의 변경이 많으면 쿼리는 기본적으로 7일 Time Travel 기능을 제공하고 있어 Physical Bytes는 7일동안 변경 시각의 데이터들이 디스크에 압축되어 모두 저장.
- 결론: GCP BigQuery는 기본적으로 Logical을 기준으로 과금. 따라서 Logical Bytes를 기준으로 모니터링 진행
# 관련 글
* [INFORMATION_SCHEMA](https://rho715.github.io/gcp/INFORMATION_SCHEMA/) -> INFORMATION_SCHEMA.TABLE*

# SQL
```sql
SELECT
*
, current_datetime('Asia/Seoul') current_time
FROM
  `region-asia-northeast3`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION
```