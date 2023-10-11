---
title: 3. 추론하기
---



# OpenAI 잘사용하는 방법 

1. [[OpenAI - PE_1|프롬프트를 위한 지침]]
2. [[OpenAI - PE_2|반복 프롬프트 & 요약하기]]
3. **추론하기** 
4. [[OpenAI - PE_4|텍스트 변환]]
5. [[OpenAI - PE_5|프롬프트 확장]]
6. [[OpenAI - PE_6|챗봇]]


# 추론하기 ([ipynb](https://colab.research.google.com/drive/110CDWTIkuBMCQcAnzGvVSyK4oDnXMVia?usp=sharing))
## sentiment
```python
prompt = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
```

## information extraction is part of NLP (Natural Language Processing)  

```python
prompt = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.

Review text: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
```
## Inferring Topics 
```python
story = """
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
"""
topic_list = [
"nasa", "local government", "engineering", 
"employee satisfaction", "federal government"
]

prompt = f"""
Determine whether each item in the following list of \
topics is a topic in the text below, which
is delimited with triple backticks.

Give your answer as list with 0 or 1 for each topic.\

List of topics: {", ".join(topic_list)}

Text sample: '''{story}'''
"""
response = get_completion(prompt)
print(response)

# just a warning use JSON instead of list
topic_dict = {i.split(': ')[0]: int(i.split(': ')[1]) for i in response.split(sep='\n')}
if topic_dict['nasa'] == 1:
print("ALERT: New NASA story!")
```
```
nasa: 1
local government: 0
engineering: 0
employee satisfaction: 1
federal government: 1
```