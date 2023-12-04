---
title: 1. 프롬프트를 위한 지침
tags:
  - python
  - openai
  - ai
  - bookmark
---



# OpenAI 잘사용하는 방법 

1. **프롬프트를 위한 지침**
2. [[OpenAI - PE_2|반복 프롬프트 & 요약하기]]
3. [[OpenAI - PE_3|추론하기]]
4. [[OpenAI - PE_4|텍스트 변환]]
5. [[OpenAI - PE_5|프롬프트 확장]]
6. [[OpenAI - PE_6|챗봇]]


# 프롬프트를 위한 지침 ([.ipynb](https://colab.research.google.com/drive/1Zt8U-2c3oKv2C8TvchM-j3NNdu8ir74l?usp=sharing))
>[!note]
> write clear and specific instructions (separate sections)

## Use delimiters
```python
 def get_completion(prompt, model="gpt-35-turbo"):
     msg = [{"role": "user", "content": prompt}]
     rsp = openai.ChatCompletion.create(
         model=model,
         messages=msg,
         temperature=0,
     )
     return response.choices[0].message["content"]

 text = "a paragraph or text that you want to summarize"

 prompt = f"""
 Summarize the text delimited by triple quotes \ 
 into a single sentence 
 '''{text}'''
 """

 rsp = get_completion(prompt)
 print(rsp)
```

## Ask for structured output
 ```python
 prompt = f"""
 Generate a list of three made-up book titles along \ 
 with their authors and genres. 
 Provide them in JSON format with the following keys:
 book_id, title, author, gnere.
 """
 ```

## Check whether conditions are satisfied 
 ```python
 text_1 = f"""
 Making a cup of tea is easy! First, you need to get some \
 water boiling. While that's happening, \
 grab a cup and put a tea bag in it. Once the water is \
 hot enough, just pour it over the tea bag. \
 Let it sit for a bit so the tea can steep. After a \
 few minutes, take out the tea bag. If you \
 like, you can add some sugar or milk to taste. \
 And that's it! You've got yourself a delicious \
 cup of tea to enjoy.
 """

 text_1 = f"""
 The sun is shining brightly today, and the birds are \
 'singing. It's a beautiful day to go for a \
 walk in the park. The flowers are blooming, and the \
 trees are swaying gently in the breeze. People \
 are out and about, enjoying the lovely weather. \
 Some are having picnics, while others are playing \
 games or simply relaxing on the grass. It's a\
 perfect day to spend time outdoors and appreciate the \
 beauty of nature.
 MORE VIDEOS
 7:29 / 17:36
 prompt = f"""

 text = text_1 
 text = text_2

 prompt = f"""
 You will be provided with text delimited by triple quotes.
 If it contains a sequence of instructions, \
 re-write those instructions in the following format:
 
 Step 1 -
 Step 2 -
 Step N - ...

 If the text does not contain a sequence of instructions, \
 then simply write \"No steps provided. \"

 \"\"\"{text}\"\"\"
 """

 response = get_completion (prompt)
 print("Completion for Text 1:")
 print (response)

 response = get_completion (prompt)
 print("Completion for Text 2:")
 print (response)


 ```

## Few-shot prompting 
 ```python
 prompt = f"""
 Your task is to answer in a consistent style.
 <child>: Teach me about patience.
 <grandparent>: The river that carves the deepest \
 valley flows from a modest spring; the \
 grandest symphony originates from a single note; \
 the most intricate tapestry begins with a solitary thread.
 <child>: Teach me about resilience.
 """
 ```

## Give the model time to think: Specify the steps to complete a task 
 ```python
 text = f"""
 In a charming village, siblings Jack and Jill set out on \ 
 a quest to fetch water from a hilltop \ 
 well. As they climbed, singing joyfully, misfortune \ 
 struck—Jack tripped on a stone and tumbled \ 
 down the hill, with Jill following suit. \ 
 Though slightly battered, the pair returned home to \ 
 comforting embraces. Despite the mishap, \ 
 their adventurous spirits remained undimmed, and they \ 
 continued exploring with delight.
 """
 # example 1
 prompt_1 = f"""
 Perform the following actions: 
 1 - Summarize the following text delimited by triple \
 backticks with 1 sentence.
 2 - Translate the summary into French.
 3 - List each name in the French summary.
 4 - Output a json object that contains the following \
 keys: french_summary, num_names.

 Separate your answers with line breaks.

 Text:
 ```{text}```
 """
 response = get_completion(prompt_1)
 print("Completion for prompt 1:")
 print(response)
 ```


 ```python
 prompt_2 = f"""
 Your task is to perform the following actions: 
 1 - Summarize the following text delimited by 
 <> with 1 sentence.
 2 - Translate the summary into French.
 3 - List each name in the French summary.
 4 - Output a json object that contains the 
 following keys: french_summary, num_names.

 Use the following format:
 Text: <text to summarize>
 Summary: <summary>
 Translation: <summary translation>
 Names: <list of names in Italian summary>
 Output JSON: <json with summary and num_names>

 Text: <{text}>
 """
 response = get_completion(prompt_2)
 print("\nCompletion for prompt 2:")
 print(response)
 ```

## Instruct the model to work out its own solution before rushing to a conclusion 
 ```python
 prompt = f"""
 Determine if the student's solution is correct or not.

 Question:
 I'm building a solar power installation and I need \
 help working out the financials. 
 - Land costs $100 / square foot
 - I can buy solar panels for $250 / square foot
 - I negotiated a contract for maintenance that will cost \ 
 me a flat $100k per year, and an additional $10 / square \
 foot
 What is the total cost for the first year of operations 
 as a function of the number of square feet.

 Student's Solution:
 Let x be the size of the installation in square feet.
 Costs:
 1. Land cost: 100x
 2. Solar panel cost: 250x
 3. Maintenance cost: 100,000 + 100x
 Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
 """
 response = get_completion(prompt)
 print(response)
 ```

 ```python
 prompt = f"""
 Your task is to determine if the student's solution \
 is correct or not.
 To solve the problem do the following:
 - First, work out your own solution to the problem. 
 - Then compare your solution to the student's solution \ 
 and evaluate if the student's solution is correct or not. 
 Don't decide if the student's solution is correct until 
 you have done the problem yourself.

 Use the following format:
 Question:
 \```
 question here
 \```
 Student's solution:
 \```
 student's solution here
 \```
 Actual solution:
 \```
 steps to work out the solution and your solution here
 \```
 Is the student's solution the same as actual solution \
 just calculated:
 \```
 yes or no
 \```
 Student grade:
 \```
 correct or incorrect
 \```

 Question:
 \```
 I'm building a solar power installation and I need help \
 working out the financials. 
 - Land costs $100 / square foot
 - I can buy solar panels for $250 / square foot
 - I negotiated a contract for maintenance that will cost \
 me a flat $100k per year, and an additional $10 / square \
 foot
 What is the total cost for the first year of operations \
 as a function of the number of square feet.
 \``` 
 Student's solution:
 \```
 Let x be the size of the installation in square feet.
 Costs:
 1. Land cost: 100x
 2. Solar panel cost: 250x
 3. Maintenance cost: 100,000 + 100x
 Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
 \```
 Actual solution:
 """
 response = get_completion(prompt)
 print(response)
 ```

# Model Limitations
1. hallucination: in order to reduce hallucinations, fist find relevant information, then answer the question based on the relevant information. 

# 참고자료
- [ChatGPT Prompt Engineering for Developers - DeepLearning.AI](https://www.youtube.com/playlist?list=PLSpnHWTONcJ3Hiecy_6nprwhKyJv40U6M)
- [Best practices for prompt engineering with OpenAI API](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api)
- [Azure OpenAI GPT-4 Tutorial](https://www.youtube.com/watch?v=uCKH8bmPgFs)
- [ChatGPT 및 GPT-4 모델 작업 방법 알아보기(미리 보기)](https://learn.microsoft.com/ko-kr/azure/cognitive-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions)
- [OpenAI's NEW ChatGPT API (gpt-3.5-turbo) - Handling Token Limits](https://www.youtube.com/watch?v=xkCzP4-YoNA)

