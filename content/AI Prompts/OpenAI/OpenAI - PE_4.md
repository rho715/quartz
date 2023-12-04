---
title: 🤖 4. 텍스트 변환
tags:
  - python
  - openai
  - ai
---

# OpenAI 잘사용하는 방법 

1. [[OpenAI - PE_1|프롬프트를 위한 지침]]
2. [[OpenAI - PE_2|반복 프롬프트 & 요약하기]]
3. [[OpenAI - PE_3|추론하기]]
4. **텍스트 변환**
5. [[OpenAI - PE_5|프롬프트 확장]]
6. [[OpenAI - PE_6|챗봇]]


# 텍스트 변환 ([ipynb](https://colab.research.google.com/drive/1pN-9psJQ4pmpgn0d4AJsY7QgwD45Ef7_?usp=sharing))

## Translation 
```python
user_messages = [
"La performance du système est plus lente que d'habitude.",  # System performance is slower than normal         
"Mi monitor tiene píxeles que no se iluminan.",              # My monitor has pixels that are not lighting
"Il mio mouse non funziona",                                 # My mouse is not working
"Mój klawisz Ctrl jest zepsuty",                             # My keyboard has a broken control key
"我的屏幕在闪烁"                                               # My screen is flashing
] 
for issue in user_messages:
prompt = f"Tell me what language this is: ```{issue}```"
lang = get_completion(prompt)
print(f"Original message ({lang}): {issue}")

prompt = f"""
Translate the following  text to English \
and Korean: ```{issue}```
"""
response = get_completion(prompt)
print(response, "\n")
```
```
Original message (This is French.): La performance du système est plus lente que d'habitude.
English: The system performance is slower than usual.
Korean: 시스템 성능이 평소보다 느립니다. 

Original message (This is Spanish.): Mi monitor tiene píxeles que no se iluminan.
English: My monitor has pixels that don't light up.
Korean: 내 모니터에는 불이 켜지지 않는 픽셀이 있습니다. 

Original message (This is Italian.): Il mio mouse non funziona
English: My mouse is not working.
Korean: 내 마우스가 작동하지 않습니다. 

Original message (This is Polish.): Mój klawisz Ctrl jest zepsuty
English: My Ctrl key is broken.
Korean: 제 Ctrl 키가 고장 났어요. 

Original message (This is Chinese (Simplified).): 我的屏幕在闪烁
English: My screen is flickering.
Korean: 내 화면이 깜빡입니다. 
```

## Writing (Change its tone/style)
- formal vs informal 
- slang -> business 

## Input / Output Formats 
```python
data_json = { "resturant employees" :[ 
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

prompt = f"""
Translate the following python dictionary from JSON to an HTML \
table with column headers and title: {data_json}
"""
response = get_completion(prompt)
print(response)
from IPython.display import display, Markdown, Latex, HTML, JSON
display(HTML(response))
```
## Grammar & Spelling Check 
```python
text = [ 
"The girl with the black and white puppies have a ball.",  # The girl has a ball.
"Yolanda has her notebook.", # ok
"Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
"Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
"Your going to need you’re notebook.",  # Homonyms
"That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
"This phrase is to cherck chatGPT for speling abilitty"  # spelling
]
for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""
    response = get_completion(prompt)
    print(response)
```
```python
text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
prompt = f"proofread and correct this review: ```{text}```"
response = get_completion(prompt)
print(response)
from redlines import Redlines

diff = Redlines(text,response)
display(Markdown(diff.output_markdown))
```