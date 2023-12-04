---
title: 🐍 Dates (Python)
tags:
  - python
  - datetime
  - date
---

# Python datetime & timezone 뽀개기
## 설명

- strftime : is used to convert a datetime object to a string (datetime -> string)
- strptime : is used to convert a string to a datetime object (string -> datetime)

``` python 
import datetime

dt = datetime.datetime(2022, 12, 12)
s = dt.strftime("%Y-%m-%d")
print(s)  # prints "2022-12-12"

import datetime

s = "2022-12-12"
dt = datetime.datetime.strptime(s, "%Y-%m-%d")
print(dt)  # prints "2022-12-12 00:00:00"
```

### Examples
#### string -> date & date -> string 
```python 
from datetime import datetime, timedelta, timezone

print( "#from string to date")
yyyymmdd_str = '20221212'
yyyymmdd_date = datetime.strptime(yyyymmdd_str, '%Y%m%d').date()

print(yyyymmdd_str, "type is", type(yyyymmdd_str))
print(yyyymmdd_date, "type is", type(yyyymmdd_date))

print("\n#from date to string")
yyyymmdd_date = datetime(2022, 12, 12)
yyyymmdd_str = yyyymmdd_date.strftime("%Y-%m-%d")

print(yyyymmdd_str, "type is", type(yyyymmdd_str))
print(yyyymmdd_date, "type is", type(yyyymmdd_date))
```
> #from string to date   
> 20221212 type is <class 'str'>   
> 2022-12-12 type is <class 'datetime.date'> 

> #from date to string   
> 2022-12-12 type is <class 'str'>   
> 2022-12-12 00:00:00 type is <class 'datetime.datetime'>   

#### timezone
```python 
from datetime import datetime, timedelta, timezone

timestamp_now_UTC = datetime.now()
timestamp_now_KST = datetime.now(timezone(timedelta(hours=9)))

print("timestamp_now_UTC : ", timestamp_now_UTC)
print("timestamp_now_KST : ", timestamp_now_KST)
```
> timestamp_now_UTC :  2022-12-30 16:14:48.156993   
> timestamp_now_KST :  2022-12-30 16:14:48.157021+09:00   

```python 
from datetime import datetime, timedelta, timezone

timezone_kst = timezone(timedelta(hours=9))

# UTC -> KST 
timestamp_UTC = datetime(2022, 12, 12,  1, 1, 1)
print("timestamp_UTC : ", timestamp_UTC, type(timestamp_UTC))
timestamp_KST = timestamp_UTC.astimezone(timezone_kst)
print("timestamp_KST : ", timestamp_KST, type(timestamp_KST))
```
> timestamp_UTC :  2022-12-12 01:01:01 <class 'datetime.datetime'>   
> timestamp_KST :  2022-12-12 01:01:01+09:00 <class 'datetime.datetime'>    

```python 
from datetime import datetime, timedelta, timezone

timezone_utc = timezone.utc 

# KST -> UTC
timestamp_KST = datetime(2022, 12, 12,  1, 1, 1)
print("timestamp_KST : ", timestamp_KST, type(timestamp_KST))
timestamp_UTC = timestamp_KST.astimezone(timezone_utc)
print("timestamp_UTC : ", timestamp_UTC, type(timestamp_UTC))
```
> timestamp_KST :  2022-12-12 01:01:01 <class 'datetime.datetime'>   
> timestamp_UTC :  2022-12-11 16:01:01+00:00 <class 'datetime.datetime'>   

```python   
from datetime import datetime, timedelta, timezone

timezone_utc = timezone.utc 

timestamp_KST = datetime(2022, 12, 12,  1, 1, 1)
timestamp_UTC = timestamp_KST.astimezone(timezone_utc)

delta = timedelta(days=1)

query_date_UTC = timestamp_UTC - delta
query_date_KST = timestamp_KST - delta

print("\nquery_date_UTC : from datetime -> string")
yyyy, mm, dd = (query_date_UTC.strftime('%Y'), query_date_UTC.strftime('%m'), query_date_UTC.strftime('%d'))
yyyymmdd, yyyy_mm_dd = (query_date_UTC.strftime('%Y%m%d'), query_date_UTC.strftime('%Y-%m-%d'))
hh = query_date_UTC.strftime('%H')  # 시
print(yyyymmdd, hh)

print("\nquery_date_KST : from datetime -> string")
yyyy, mm, dd = (query_date_KST.strftime('%Y'), query_date_KST.strftime('%m'), query_date_KST.strftime('%d'))
yyyymmdd, yyyy_mm_dd = (query_date_KST.strftime('%Y%m%d'), query_date_KST.strftime('%Y-%m-%d'))
hh = query_date_KST.strftime('%H')  # 시
print(yyyymmdd, hh)
```
> query_date_UTC : from datetime -> string  
> 20221210 16

> query_date_KST : from datetime -> string  
> 20221211 01


#### pandas 

```python 
import pandas as pd 
import numpy as np 

#date range
datelist_periods= pd.date_range('20160701', periods = 6).tolist()
datelist_from_to = pd.date_range('20160701', '20160703').tolist()

print("printing datelist_periods")
print(*datelist_periods, sep = '\n')
print("\nprinting datelist_from_to")
print(*datelist_from_to, sep = '\n')
 
```
> printing datelist_periods  
> 2016-07-01 00:00:00  
> 2016-07-02 00:00:00  
> 2016-07-03 00:00:00  
> 2016-07-04 00:00:00  
> 2016-07-05 00:00:00  
> 2016-07-06 00:00:00  

> printing datelist_from_to  
> 2016-07-01 00:00:00  
> 2016-07-02 00:00:00  
> 2016-07-03 00:00:00  

```python 
import pandas as pd 
import numpy as np 

#date range
df = pd.DataFrame(np.random.randn(6,4))
df.index = pd.date_range('20160701', periods = 6)
df['yyyy_mm_dd'] = pd.date_range('20160701', periods = 6) #datetime
df['yyyy'] = pd.to_datetime("2022", format='%Y')
df['mm'] = pd.to_datetime("02", format='%m')
df['Yr_Mo_dy'] = '2022-12-11'
df['Yr_Mo_dy_edit'] = df['Yr_Mo_dy'].apply(pd.to_datetime)
 
display(df)
df.info()
```

