---
title: . Dates (SQL)
tags:
  - sql
  - date
  - datetime
---

# SQL datetime & timezone 뽀개기
## 설명

```sql 
  

WITH my_table AS (
SELECT "2022-07-27 15:30:45" AS timestamp_str UNION ALL
SELECT "2022-08-10 08:00:00" AS timestamp_str
)

SELECT
-- input string: PARSE_DATE
-- input date/time: FORMAT_DATE

-- Original timestamp string in string format
timestamp_str AS original_timestamp,

-- str -> timestamp
PARSE_DATETIME('%Y-%m-%d %H:%M:%S', timestamp_str) AS parsed_timestamp,

-- str -> datetime -> str
FORMAT_DATETIME('%b %d, %Y - %I:%M %p', PARSE_DATETIME('%Y-%m-%d %H:%M:%S', timestamp_str)) AS formatted_timestamp

FROM my_table;

```


>  original_timestamp	 | parsed_timestamp |	formatted_timestamp   
>  2022-07-27 15:30:45	| 2022-07-27T15:30:45 | "Jul 27, 2022 - 03:30 PM"   
>  2022-08-10 08:00:00 | 2022-08-10T08:00:00 | "Aug 10, 2022 - 08:00 AM"