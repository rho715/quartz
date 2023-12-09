---
title: _. LangChain Basic Codes
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


# also same as the code below

# template = PromptTemplate(
# 			 template="What is the difference between {country1} and {country2}?",
# 			 input_variables=["country1", "country2"],
# )
# prompt = template.format(country1="Mexico", country2="Thailand")


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

## Using `FewShotPromptTemplate`
```python
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

examples = [
    {
        "question": "What do you know about France?",
        "answer": """
        Here is what I know:
        Capital: Paris
        Language: French
        Food: Wine and Cheese
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Italy?",
        "answer": """
        I know this:
        Capital: Rome
        Language: Italian
        Food: Pizza and Pasta
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Greece?",
        "answer": """
        I know this:
        Capital: Athens
        Language: Greek
        Food: Souvlaki and Feta Cheese
        Currency: Euro
        """,
    },
]


example_prompt = PromptTemplate.from_template("Human: {question}\nAI:{answer}")

prompt = FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
    suffix="Human: What do you know about {country}?",
    input_variables=["country"],
)

chain = prompt | llm

chain.invoke({"country": "Turkey"})
```

## Using `LengthBasedExampleSelector`
- example 허용 길이 설정 
```python 
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector

examples = [
    {
        "question": "What do you know about France?",
        "answer": """
        Here is what I know:
        Capital: Paris
        Language: French
        Food: Wine and Cheese
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Italy?",
        "answer": """
        I know this:
        Capital: Rome
        Language: Italian
        Food: Pizza and Pasta
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Greece?",
        "answer": """
        I know this:
        Capital: Athens
        Language: Greek
        Food: Souvlaki and Feta Cheese
        Currency: Euro
        """,
    },
]


example_prompt = PromptTemplate.from_template("Human: {question}\nAI:{answer}")

example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    max_length=80, # <- this is the max length of the example prompt
)

prompt = FewShotPromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    suffix="Human: What do you know about {country}?",
    input_variables=["country"],
)
prompt.format(country="Turkey")

# chain = prompt | llm
# chain.invoke({"country": "Turkey"})
```
## Using `RandomExampleSelector`
```python
from langchain.prompts import example_selector
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts.example_selector.base import BaseExampleSelector

examples = [
    {
        "question": "What do you know about France?",
        "answer": """
        Here is what I know:
        Capital: Paris
        Language: French
        Food: Wine and Cheese
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Italy?",
        "answer": """
        I know this:
        Capital: Rome
        Language: Italian
        Food: Pizza and Pasta
        Currency: Euro
        """,
    },
    {
        "question": "What do you know about Greece?",
        "answer": """
        I know this:
        Capital: Athens
        Language: Greek
        Food: Souvlaki and Feta Cheese
        Currency: Euro
        """,
    },
]


class RandomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)

    def select_examples(self, input_variables):
        from random import choice

        return [choice(self.examples)]


example_prompt = PromptTemplate.from_template("Human: {question}\nAI:{answer}")

example_selector = RandomExampleSelector(
    examples=examples,
)

prompt = FewShotPromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
    suffix="Human: What do you know about {country}?",
    input_variables=["country"],
)

prompt.format(country="Brazil")
```
## Using `FewShotChatPromptTemplate`
```python
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatMessagePromptTemplate, ChatPromptTemplate


examples = [
    {
        "country": "France",
        "answer": """
        Here is what I know:
        Capital: Paris
        Language: French
        Food: Wine and Cheese
        Currency: Euro
        """,
    },
    {
        "country": "Italy",
        "answer": """
        I know this:
        Capital: Rome
        Language: Italian
        Food: Pizza and Pasta
        Currency: Euro
        """,
    },
    {
        "country": "Greece",
        "answer": """
        I know this:
        Capital: Athens
        Language: Greek
        Food: Souvlaki and Feta Cheese
        Currency: Euro
        """,
    },
]


example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "What do you know about {country}?"),
        ("ai", "{answer}"),
    ]
)

example_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a geography expert, you give short answers."),
        example_prompt,
        ("human", "What do you know about {country}?"),
    ]
)

chain = final_prompt | llm

chain.invoke({"country": "Thailand"})
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

# Prompt Files
---
## Load Prompts
- importing `prompt.json`
```json
{
    "_type": "prompt", 
    "template": "What is the captial of {country}?",
    "input_variables": ["country"],
}
```

```python
from langchain.prompts import load_prompt
prompt = load_prompt("./prompt.json")
prompt.format(country="Brazil")
```

- importing `prompt.yaml`
```yaml
_type: "prompt"
template: "What is the captial of {country}?"
input_variables: ["country"]
```

```python
from langchain.prompts import load_prompt
prompt = load_prompt("./prompt.yaml")
prompt.format(country="Brazil")
```

## Prompts Composition

- combine prompts
```python
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate



intro = PromptTemplate.from_template(
    """
    You are a role playing assistant.
    And you are impersonating a {character}
"""
)

example = PromptTemplate.from_template(
    """
    This is an example of how you talk:

    Human: {example_question}
    You: {example_answer}
"""
)

start = PromptTemplate.from_template(
    """
    Start now!

    Human: {question}
    You:
"""
)

final = PromptTemplate.from_template(
    """
    {intro}
                                     
    {example}
                              
    {start}
"""
)

prompts = [
    ("intro", intro),
    ("example", example),
    ("start", start),
]


full_prompt = PipelinePromptTemplate(
    final_prompt=final,
    pipeline_prompts=prompts,
)


full_prompt.format(
        character="Pirate",
        example_question="What is your location?",
        example_answer="Arrrrg! That is a secret!! Arg arg!!",
        question="What is your fav food?"
)

    
```
- using chain 
```python
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.prompts.pipeline import PipelinePromptTemplate



intro = PromptTemplate.from_template(
    """
    You are a role playing assistant.
    And you are impersonating a {character}
"""
)

example = PromptTemplate.from_template(
    """
    This is an example of how you talk:

    Human: {example_question}
    You: {example_answer}
"""
)

start = PromptTemplate.from_template(
    """
    Start now!

    Human: {question}
    You:
"""
)

final = PromptTemplate.from_template(
    """
    {intro}
                                     
    {example}
                              
    {start}
"""
)

prompts = [
    ("intro", intro),
    ("example", example),
    ("start", start),
]


full_prompt = PipelinePromptTemplate(
    final_prompt=final,
    pipeline_prompts=prompts,
)


chain = full_prompt | llm 

chain.invoke(
    {
        "character": "Pirate",
        "example_question": "What is your location?",
        "example_answer": "Arrrrg! That is a secret!! Arg arg!!",
        "question": "What is your fav food?",
    }
)
```

# Cache
---
```python
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.globals import set_llm_cache, set_debug
from langchain.cache import InMemoryCache, SQLiteCache

#set_llm_cache(InMemoryCache())
set_llm_cache(SQLiteCache("cache.db")) # <- this will create a cache.db file in the current directory
set_debug(True)


llm.predict("How do you make italian pasta") # 34.3s & 0.0
```

# `Usage`
---
```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as usage: # <- this will print the usage of the API that is under the with statement
    a = llm.predict("What is the recipe for soju")
    b = llm.predict("What is the recipe for bread")
    print(a, "\n")
    print(b, "\n")
    print(usage)
```

# Model Settings 
---
## Save `model.json`
```python
from langchain.llms.openai import OpenAI

chat = OpenAI(temperature=0.1, max_tokens=450)
chat.save("model.json")
```

## Result 
```json 
{
    "model_name": "gpt-3.5-turbo-16k",
    "temperature": 0.1,
    "max_tokens": 450,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "n": 1,
    "request_timeout": null,
    "logit_bias": {},
    "_type": "openai"
}
```

## Load `model.json`
```python
from langchain.llms.loading import load_llm

chat = load_llm("model.json")
```