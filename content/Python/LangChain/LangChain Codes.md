---
title: _. LangChain Codes
tags:
  - python
  - langchain
  - ai
  - openai
---
# Importing `AzureChatOpenAI()`
----
## set your `.env` file first
```
OPENAI_API_TYPE="azure"
OPENAI_API_BASE="https://{url}.openai.azure.com/"
OPENAI_API_VERSION="2023-07-01-preview"
OPENAI_API_KEY="{your_key}"
```

## when `langchain<= 0.0.332`
```python

from langchain.chat_models import AzureChatOpenAI
import os 

llm = AzureChatOpenAI(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_type=os.getenv("OPENAI_API_TYPE"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_name="gpt-4",
    deployment_name="gpt-4-turbo",
    temperature=0,
    model_version="1106-Preview",
    # model_kwargs={"streaming": True},
)
```
## when `langchain >=0.0.345`
```python
from langchain.chat_models import AzureChatOpenAI
import os 

llm = AzureChatOpenAI(  
    openai_api_key=os.getenv("OPENAI_API_KEY"),  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  
    openai_api_version=os.getenv("OPENAI_API_VERSION"),  
    model_name="gpt-4",  
    deployment_name="gpt-4-turbo",  
    temperature=0,  
    model_version="1106-Preview",  
    # model_kwargs={"streaming": True},  
)
```

# Simple Trigger 
---
## String 
```python
llm.predict("what are the cities in Korea")
```

## Messages
```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage

messages = [
    SystemMessage(
        content="You are a geography expert. And you only reply in Italian.",   
    ),
    AIMessage(content="Ciao, mi chiamo Rhorho!"),
    HumanMessage(content="What is the distance between Mexico and Thailand? Also, what is your name?")
]

llm.predict_messages(messages)
```

# Using Templates
---
## Using `PromptTemplate`
```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
 
template = PromptTemplate.from_template("what is the difference between {country1} and {country2}?")
prompt = template.format(country1="Mexico", country2="Thailand")

llm.predict(prompt)
```

## Using `ChatPromptTemplate`
```python
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate, ChatPromptTemplate
 
template = ChatPromptTemplate.from_messages([
    ("system", "You are a geography expert. And you only reply in {language}."),
    ("ai", "Ciao, mi chiamo Rhorho!"),
    ("human", "What is the distance between {country1} and {country2}? Also, what is your name?")
])

prompt = template.format_messages(
    language="Italian",
    country1="Mexico",
    country2="Thailand",
    name="Rhorho"
)

llm.predict_messages(prompt)
```

# Parser
---
```python
from langchain.schema import BaseOutputParser

class CommaOutputParser(BaseOutputParser):
    def parse(self, text):
        items = text.strip().split(",")
        return list(map(str.strip,items))

p = CommaOutputParser()
p.parse("hllo, world") 
```


# LCEL 
---
- 참고하면 좋은 기록: [[LCEL]]
## Not Using LCEL
```python
# not using LCEL
template = ChatPromptTemplate.from_messages([
    ("system", "You are a list generating machine. \
     Everything you are asked will be answered with a comma separated list of max {max_items} in lower case. \
     Do NOT reply with anything else."),
     ("human", "{question}")
])

prompt = template.format_messages(
    max_items=5,
    question="What are planets?"
)
result = llm.predict_messages(prompt)

p.parse(result.content)
```

## Using LCEL
```python
# using LCEL
template = ChatPromptTemplate.from_messages([
    ("system", "You are a list generating machine. \
     Everything you are asked will be answered with a comma separated list of max {max_items} in lower case. \
     Do NOT reply with anything else."),
     ("human", "{question}")
])

chain = template | llm | CommaOutputParser()

chain.invoke({"max_items":5, "question":"What are cities in Korea?"})
```


# Applications (multiple chains & streaming)
---
```python
from langchain.callbacks import StreamingStdOutCallbackHandler
llm_streaming = AzureChatOpenAI(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_type=os.getenv("OPENAI_API_TYPE"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    model_name="gpt-4",
    deployment_name="gpt-4-turbo",
    temperature=0,
    model_version="1106-Preview",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
    
chef_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world-class international chef. \
     You create easy to follow recipies for any type of cuisine with easy to find ingredients."),
     ("human", "I want to make {dish}"),
])

chef_chain = chef_prompt | llm_streaming  

chef_prompt_veg = ChatPromptTemplate.from_messages([
    ("system", "You are a vegetarian chef specialized on making traditional recipies vegetarian.\
      You find alternative ingredients and explain their preparation. \
     You don't radically modify the recipe. \
     If there is no alternative for a food just say you don't know how to replace it."),
    ("human", "{recipe}")
])

chain_veg = chef_prompt_veg | llm_streaming

final_chain = {"recipe": chef_chain} | chain_veg

final_chain.invoke({"dish":"kimchi jjigae"})
```