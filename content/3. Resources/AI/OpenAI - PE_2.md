---
title: 2. 반복 프롬프트 & 요약하기
tags:
  - python
  - openai
  - AI
---



# OpenAI 잘사용하는 방법 

1. [[OpenAI - PE_1|프롬프트를 위한 지침]]
2. **반복 프롬프트** & **요약하기**
3. [[OpenAI - PE_3|추론하기]]
4. [[OpenAI - PE_4|텍스트 변환]]
5. [[OpenAI - PE_5|프롬프트 확장]]
6. [[OpenAI - PE_6|챗봇]]


# 반복 프롬프트 ([ipynb](https://colab.research.google.com/drive/1kolj2HPakI43DU3BOug_wEP-wQ_UCAq4?usp=sharing))

-  Idea -> Implementation (code/data) -> Experimental result -> Error Analysis 
- AI doesn't really work well with numbers 
- Iterative Process 
    1. Try something 
    2. Analyze where the result does nto give what you want 
    3. Clarify instructions, give more time to think 
    4. Refine prompts with a batch of examples 

# 요약하기 ([ipynb](https://colab.research.google.com/drive/1KmtI-ZI3bY_eWiXpqMw_TeNxz53smCu2?usp=sharing))

```python
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""

prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)


prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the pricing department. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words and focusing on any aspects that \ 
are relevant to the price and perceived value. 

Review: ```{prod_review}```
"""

response = get_completion(prompt)
print(response)

```

# 참고자료
- [ChatGPT Prompt Engineering for Developers - DeepLearning.AI](https://www.youtube.com/playlist?list=PLSpnHWTONcJ3Hiecy_6nprwhKyJv40U6M)
