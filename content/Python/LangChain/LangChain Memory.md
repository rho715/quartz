---
title: _. LangChain Memory
tags:
  - ai
  - langchain
  - python
  - openai
---
![[LangChain Basic Codes#Importing `AzureChatOpenAI()`]]
# Using Memory
## `ConversationBufferMemory`
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,
)

memory.save_context({"input": "Hi"}, {"output": "Hello"})   

memory.load_memory_variables({})
```
>  `{'history': [HumanMessage(content='Hi'), AIMessage(content='Hello')]}`

## `ConversationBufferWindowMemory`
- save up to last `n` messages (most recent)
```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    return_messages=True,
    k=2,
)

def add_message(input, output):
	memory.save_context({"input": input}, {"output": output})

add_messages(1,1)
add_messages(2,2)
add_messages(3,3)

memory.load_memory_variables({})
```
>  {'history': [HumanMessage(content='2'), AIMessage(content='2'), 
>  HumanMessage(content='3'), AIMessage(content='3')]}

## `ConversationSummaryMemory`
```python
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI

memory = ConversationSummaryMemory(llm=llm)

def add_message(input, output):
    memory.save_context({"input": input}, {"output": output})

def get_history():
    return memory.load_memory_variables({})

add_message("Hi I'm Nicolas, I live in South Korea", "Wow that is so cool!")
add_message("South Kddorea is so pretty", "I wish I could go!!!")
get_history()
```
> `{'history': 'Nicolas introduces himself and mentions he lives in South Korea, which he finds pretty, and the AI enthusiastically wishes it could visit.'}`


```python
from operator import itemgetter
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful chatbot"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{message}"),
    ]
)

memory = ConversationBufferMemory(return_messages=True)

def load_memory(_):
    x = memory.load_memory_variables({})
    return {"history": x["history"]}

chain = RunnablePassthrough.assign(history=load_memory) | prompt | llm

inputs = {"message": "hi im bob"}
response = chain.invoke(inputs)
response
```

```run-python
1+1
```
