---
title: BigQuery JOBS_BY
tags:
  - SQL
  - BigQuery
---
# JOBS_BY_FOLDER 

```sql 
SELECT
      -- usage_time is used for grouping jobs by the hour
      -- usage_date is used to separately store the date this job occurred
      format_timestamp('%F %H:%M:00', TIMESTAMP_ADD(TIMESTAMP(jbf.creation_time), INTERVAL 9 HOUR)) AS usage_hhmm,
      EXTRACT(DATE from TIMESTAMP_ADD(TIMESTAMP(jbf.creation_time), INTERVAL 9 HOUR) ) AS usage_date,
      -- jbf.reservation_id,
      jbf.project_id,
      jbf.job_id,
      TIMESTAMP_ADD(TIMESTAMP(jbf.start_time), INTERVAL 9 HOUR) start_time,
      TIMESTAMP_ADD(TIMESTAMP(jbf.end_time), INTERVAL 9 HOUR) end_time,
      timestamp_diff(TIMESTAMP_ADD(TIMESTAMP(jbf.end_time), INTERVAL 9 HOUR), TIMESTAMP_ADD(TIMESTAMP(jbf.start_time), INTERVAL 9 HOUR), second) as job_duration_s,
      timestamp_diff(TIMESTAMP_ADD(TIMESTAMP(jbf.end_time), INTERVAL 9 HOUR), TIMESTAMP_ADD(TIMESTAMP(jbf.start_time), INTERVAL 9 HOUR), millisecond) as job_duration_ms,
      jbf.state,
      jbf.total_bytes_processed, 
      jbf.job_type,
      jbf.user_email,
      jbf.error_result.reason error_result_reason,
      jbf.error_result.message error_result_message,
      -- Aggregate total_slots_ms used for all jobs at this hour and divide
      -- by the number of milliseconds in an hour. Most accurate for hours with
      -- consistent slot usage
      SUM(jbf.total_slot_ms) / (1000 * 60 * 60 * 60) AS average_slot_usage_per_min
    FROM
      `region-asia-northeast3`.INFORMATION_SCHEMA.JOBS_BY_FOLDER jbf
    where date(TIMESTAMP_ADD(TIMESTAMP(jbf.creation_time), INTERVAL 9 HOUR)) >= date_sub(current_date('Asia/Seoul'), interval 30 day)
    GROUP BY
      usage_date,
      usage_hhmm,
      jbf.project_id,
      jbf.job_id,
      start_time,
      end_time,
      job_duration_s,
      job_duration_ms,
      jbf.state,
      jbf.total_bytes_processed, 
      jbf.job_type,
      jbf.user_email,
      jbf.error_result.reason,
      jbf.error_result.message 
```
# JOBS_BY_PROJECT 

```sql 
select distinct
      TIMESTAMP_ADD(TIMESTAMP(creation_time), INTERVAL 9 HOUR) creation_time
      , format_timestamp('%F %H:%M:00', TIMESTAMP_ADD(TIMESTAMP(creation_time), INTERVAL 9 HOUR)) creation_hhmm
      , format_timestamp('%F %H:00:00', TIMESTAMP_ADD(TIMESTAMP(creation_time), INTERVAL 9 HOUR)) creation_hh
      , project_id
      , user_email
      , case when regexp_contains(user_email, 'gserviceaccount.com') then 'service' else 'private' end as account_type
      , job_id
      , TIMESTAMP_ADD(TIMESTAMP(start_time), INTERVAL 9 HOUR) start_time
      , TIMESTAMP_ADD(TIMESTAMP(end_time), INTERVAL 9 HOUR) end_time
      , timestamp_diff(end_time, start_time, second) as query_sec
      , timestamp_diff(end_time, start_time, millisecond) as query_ms
      , state
      , query
      , total_bytes_processed
      , total_slot_ms
      , total_slot_ms / 1000 as total_slot_s
      , safe_divide(total_slot_ms, timestamp_diff(end_time, start_time, millisecond)) as avg_slot
      , error_result.reason error_result_reason
      , error_result.message error_result_message
      , case when error_result.reason is null then 'COMPLETE' else 'ERROR' end as job_status

from `region-asia-northeast3`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
where date(timestamp_add(TIMESTAMP(creation_time), INTERVAL 9 HOUR)) >= date_sub(current_date('Asia/Seoul'), interval 30 day)
```
- you can check actual query from `jobs_by_project`
# JOBS_BY_ORGANIZATION
```sql
SELECT distinct TIMESTAMP_ADD(TIMESTAMP(creation_time), INTERVAL 9 HOUR) creation_time
        , project_id
        , user_email
        , job_id 
        , total_slot_ms
    FROM `region-asia-northeast3`.INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION
    WHERE state = 'RUNNING'
    order by total_slot_ms
```
- get currently running query


# Slot Calculation

- *How to Calculate `average_daily_slot_usage`*
	- `SUM(jbo.total_slot_ms) / (1000 * 60 * 60 * 24)`: (ms * sec * min * hour)
	- [link](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/dashboards/system_tables/docs/daily_utilization.md)

- *How to Calculate `average_hourly_slot_usage`*
	 - `SUM(jbo.total_slot_ms) / (1000 * 60 * 60)`: (ms * sec * min)
	 - [link](https://github.com/GoogleCloudPlatform/bigquery-utils/blob/master/dashboards/system_tables/docs/hourly_utilization.md)