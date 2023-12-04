---
title: _. BigQuery JSON
tags:
  - json
  - bigquery
  - sql
---

# Using function to clean json data

```python
from google.cloud import bigquery

location = "asia-northeast3"
my_account = "# rho715"

def runQuery_DF(query):
    final_query = "\n".join([my_account, query]) #add my account info to query input

    client = bigquery.Client(location=location)
    data = client.query(final_query).to_dataframe() #run query
    client.close()

    print('\nquery : ' , final_query)
    return data

query = '''
CREATE TEMP FUNCTION del_json_field(json_str STRING, key_name STRING)
RETURNS STRING
LANGUAGE js
AS r"""
  json_obj = JSON.parse(json_str)
  delete json_obj[key_name]
  return JSON.stringify(json_obj)
""";

select 
  '{"appVer":"5.0.2","carrier":"none","country":"KR","destIp":"125.132.54.23","deviceName":"Box"}' STR,
  del_json_field('{"appVer":"5.0.2","carrier":"none","country":"KR","destIp":"125.132.54.23","deviceName":"Box"}', "destIp")
;
'''
import pandas as pd
pd.set_option('display.max_colwidth', None)
runQuery_DF(query)

```

    
  
<div style="width: 100%; overflow-x: auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>STR</th>
      <th>f0_</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>{"appVer":"5.0.2","carrier":"none","country":"KR","destIp":"125.132.54.23","deviceName":"Box"}</td>
      <td>{"appVer":"5.0.2","carrier":"none","country":"KR","deviceName":"Box"}</td>
    </tr>
  </tbody>
</table>
</div>



# Using `json_extract_scalar` & `json_extract` 

```python
from google.cloud import bigquery

location = "asia-northeast3"
my_account = "# rho715"

def runQuery_DF(query):
    final_query = "\n".join([my_account, query]) #add my account info to query input

    client = bigquery.Client(location=location)
    data = client.query(final_query).to_dataframe() #run query
    client.close()

    print('\nquery : ' , final_query)
    return data

query = '''
with data_sample as (
  select
  [struct('{"action_item":"sns_share","action_param":{"optional":{"share_type":"facebook"},"required":{"id":"01_0001.1","type":"vod"}},"action_type":"button_click","current":"content_detail"}' as json_data, current_date as yyyy_mm_dd),
  struct('{"action_item":"sns_share","action_param":{"optional":{"share_type":"facebook"},"required":{"id":"01_0001.2","type":"qvod"}},"action_type":"button_click","current":"content_detail"}' as json_data, current_date as yyyy_mm_dd)
  ] as struct_sample
)
select yyyy_mm_dd
    , json_extract_scalar(json_data, '$.action_item') `action_item` --json key
    , json_extract(json_data, '$.action_param') `action_param` --json value
from data_sample, unnest(struct_sample) 
'''
import pandas as pd
pd.set_option('display.max_colwidth', None)
runQuery_DF(query)
```

    
    



<div style="width: 100%; overflow-x: auto;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>yyyy_mm_dd</th>
      <th>action_item</th>
      <th>action_param</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023-01-28</td>
      <td>sns_share</td>
      <td>{"optional":{"share_type":"facebook"},"required":{"id":"01_0001.1","type":"vod"}}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2023-01-28</td>
      <td>sns_share</td>
      <td>{"optional":{"share_type":"facebook"},"required":{"id":"01_0001.2","type":"qvod"}}</td>
    </tr>
  </tbody>
</table>
</div>



# Using `JSON_QUERY_ARRAY` & `UNNEST()`

```python
from google.cloud import bigquery

location = "asia-northeast3"
my_account = "# rho715"

def runQuery_DF(query):
    final_query = "\n".join([my_account, query]) #add my account info to query input

    client = bigquery.Client(location=location)
    data = client.query(final_query).to_dataframe() #run query
    client.close()

    print('\nquery : ' , final_query)
    return data

query = '''
with data_sample as (
  select
  [struct('{"agent":"SM-N986N","app_version":"none","data":{"action_type":"register","action_value":[{"content_id":"2101","content_type":"live"}]},"device":"android","log_timestamp":"2022-11-11 03:59:59","log_type":"","log_version":"1.2.2","profileid":"0","service":"cholo","uno":"abved","zone":"none"}' as data_json, current_timestamp() as created_at),
  struct('{"agent":"iPhone12,3","app_version":"none","data":{"action_type":"delete_all","action_value":[{"content_id":"0079","content_type":"movie"},{"content_id":"EN394","content_type":"theme"},{"content_id":"EN394","content_type":"theme"}]},"device":"ios","log_timestamp":"2022-11-10 23:58:05","log_type":"","log_version":"1.2.2","profileid":"0","service":"cholo","uno":"zdfoe","zone":"none"}' as data_json, current_timestamp() as created_at),
  struct('{"agent":"iPhone12,3","app_version":"none","data":{"action_type":"delete","action_value":[{"content_id":"0063","content_type":"program"}]},"device":"ios","log_timestamp":"2022-11-10 23:58:05","log_type":"","log_version":"1.2.2","profileid":"0","service":"cholo","uno":"jojojo","zone":"none"}' as data_json, current_timestamp() as created_at)
  ] as struct_sample
)
, struct_to_rows as (
select created_at
    , data_json 
from data_sample, unnest(struct_sample) 
)
, unnest_action_value as (
  SELECT
    JSON_QUERY_ARRAY(data_json, "$.data.action_value") `action_value_array` --array
    , created_at
    , data_json data
  FROM struct_to_rows
  WHERE
  json_extract_scalar(data_json, '$.uno') != 'test'
  and json_extract_scalar(data_json, '$.log_type') != '1.1.1'
)
select
     -- common log
     json_extract_scalar(data, '$.log_type') `log_type`  
     , json_extract_scalar(data, '$.log_timestamp') `log_timestamp`
     , TIMESTAMP_ADD(TIMESTAMP(created_at), INTERVAL 9 HOUR) `ap_timestamp` 
     , json_extract_scalar(data, '$.uno') `uno`
     , json_extract_scalar(data, '$.profileid') `profile_id`
     , json_extract_scalar(data, '$.zone') `zone`
     , json_extract_scalar(data, '$.device') `device_type`
     , json_extract_scalar(data, '$.agent') `agent`
     , json_extract_scalar(data, '$.app_version') `app_version`

     , json_extract_scalar(data, '$.data.action_type') `action_type`
     --action_value
     , json_extract_scalar(action_value, '$.content_type') `content_type`
     , json_extract_scalar(action_value, '$.content_id') `content_id`

from unnest_action_value, unnest(unnest_action_value.action_value_array) as action_value
'''
import pandas as pd
pd.set_option('display.max_colwidth', None)
runQuery_DF(query)
```

    



<div style="width: 100%; overflow-x: auto;"> <style scoped> .dataframe tbody tr th:only-of-type { vertical-align: middle; } .dataframe tbody tr th { vertical-align: top; } .dataframe thead th { text-align: right; } /* Setting specific width for columns */ .dataframe th, .dataframe td { padding: 8px 15px; /* Adding more padding for clarity */ white-space: nowrap; /* Content will be on a single line */ } /* Adjust the below widths as required */ .dataframe th:nth-child(1), .dataframe td:nth-child(1) { width: 50px; } .dataframe th:nth-child(2), .dataframe td:nth-child(2) { width: 200px; } .dataframe th:nth-child(3), .dataframe td:nth-child(3) { width: 250px; } .dataframe th:nth-child(4), .dataframe td:nth-child(4) { width: 250px; } /* ... Continue for other columns ... */ </style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>log_type</th>
      <th>log_timestamp</th>
      <th>ap_timestamp</th>
      <th>uno</th>
      <th>profile_id</th>
      <th>zone</th>
      <th>device_type</th>
      <th>agent</th>
      <th>app_version</th>
      <th>action_type</th>
      <th>content_type</th>
      <th>content_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td></td>
      <td>2022-11-11 03:59:59</td>
      <td>2023-01-28 20:51:57.011544+00:00</td>
      <td>abved</td>
      <td>0</td>
      <td>none</td>
      <td>android</td>
      <td>SM-N986N</td>
      <td>none</td>
      <td>register</td>
      <td>live</td>
      <td>2101</td>
    </tr>
    <tr>
      <th>1</th>
      <td></td>
      <td>2022-11-10 23:58:05</td>
      <td>2023-01-28 20:51:57.011544+00:00</td>
      <td>zdfoe</td>
      <td>0</td>
      <td>none</td>
      <td>ios</td>
      <td>iPhone12,3</td>
      <td>none</td>
      <td>delete_all</td>
      <td>movie</td>
      <td>0079</td>
    </tr>
    <tr>
      <th>2</th>
      <td></td>
      <td>2022-11-10 23:58:05</td>
      <td>2023-01-28 20:51:57.011544+00:00</td>
      <td>zdfoe</td>
      <td>0</td>
      <td>none</td>
      <td>ios</td>
      <td>iPhone12,3</td>
      <td>none</td>
      <td>delete_all</td>
      <td>theme</td>
      <td>EN394</td>
    </tr>
    <tr>
      <th>3</th>
      <td></td>
      <td>2022-11-10 23:58:05</td>
      <td>2023-01-28 20:51:57.011544+00:00</td>
      <td>zdfoe</td>
      <td>0</td>
      <td>none</td>
      <td>ios</td>
      <td>iPhone12,3</td>
      <td>none</td>
      <td>delete_all</td>
      <td>theme</td>
      <td>EN394</td>
    </tr>
    <tr>
      <th>4</th>
      <td></td>
      <td>2022-11-10 23:58:05</td>
      <td>2023-01-28 20:51:57.011544+00:00</td>
      <td>jojojo</td>
      <td>0</td>
      <td>none</td>
      <td>ios</td>
      <td>iPhone12,3</td>
      <td>none</td>
      <td>delete</td>
      <td>program</td>
      <td>0063</td>
    </tr>
  </tbody>
</table>
</div>











