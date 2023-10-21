---
title: "Requests Tutorial: Working With HTTP and Websites in Python"
tags:
  - http
  - request
  - python
draft:
---
[Youtube Link](https://www.youtube.com/watch?v=XqIfWkVI3UA)

[[main.py]]
```python

import requests

url = 'https://api.github.com/rho715'
response = requests.get(url)

print(response.json())
print(response.status_code)
print(response.content)

# status code
url = "https://httpbin.org/status/404"
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print("Error: {0}".format(err))

# handling errors
url = "https://www.httpbin.org/delay/10"
try:
    response = requests.get(url, timeout=2)
except requests.exceptions.Timeout as err:
    print(err)

# headers
auth_tokens = "xxx"
headers = {
    "Authorization": f"Bearer {auth_tokens}"
}

url = "https://httpbin.org/headers"
response = requests.get(url, headers=headers)
print(response.json())

# simple web scraping
# pip install beautifulsoup4
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

title = soup.title.text
content = soup.find("p").text
links = [a["href"] for a in soup.find_all("a")]

print(title, content, links)

# requests vs urllib (less intuitive)

```