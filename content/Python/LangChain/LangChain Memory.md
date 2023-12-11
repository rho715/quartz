---
title: _. LangChain Memory
tags:
  - ai
  - langchain
  - python
  - openai
---
[[LangChain Basic Codes#Importing `AzureChatOpenAI()`]]
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
>  `{'history': [HumanMessage(content='2'), AIMessage(content='2'), HumanMessage(content='3'), AIMessage(content='3')]}`

## `ConversationSummaryMemory`
```python
from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI

memory = ConversationSummaryMemory(llm=llm)

def add_message(input, output):
    memory.save_context({"input": input}, {"output": output})

def get_history():
    return memory.load_memory_variables({})

add_message("Hi I'm RhoRho, I live in South Korea", "Wow that is so cool!")
add_message("South Kddorea is so pretty", "I wish I could go!!!")
get_history()
```
> `{'history': 'RhoRho introduces himself and mentions he lives in South Korea, which he finds pretty, and the AI enthusiastically wishes it could visit.'}`

## `ConversationSummaryBufferMemory`
- when it reaches maximum token limit, then it summarizes its chat history
```python
from langchain.memory import ConversationSummaryBufferMemory

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=150,
    return_messages=True,
)

def add_message(input, output):
    memory.save_context({"input": input}, {"output": output})

def get_history():
    return memory.load_memory_variables({})

add_message("Hi I'm RhoRho, I live in South Korea", "Wow that is so cool!")
add_message("South Korea is so pretty", "I wish I could go!!!")
add_message("How far is Korea from Argentina?", "I don't know! Super far!")
add_message("How far is Brazil from Argentina?", "I don't know! Super far!")
get_history()
```
> `{'history': [HumanMessage(content="Hi I'm RhoRho, I live in South Korea"), AIMessage(content='Wow that is so cool!'), HumanMessage(content='South Korea is so pretty'), AIMessage(content='I wish I could go!!!'), HumanMessage(content='How far is Korea from Argentina?'), AIMessage(content="I don't know! Super far!"), HumanMessage(content='How far is Brazil from Argentina?'), AIMessage(content="I don't know! Super far!")]}`

## `ConversationKGMemory`
- answer questions based on history
```python

from langchain.memory import ConversationKGMemory

memory = ConversationKGMemory(
    llm=llm,
    return_messages=True,
)


def add_message(input, output):
    memory.save_context({"input": input}, {"output": output})


add_message("Hi I'm RhoRho, I live in South Korea", "Wow that is so cool!")
add_message("RhoRho likes kimchi", "Wow that is so cool!")
memory.load_memory_variables({"inputs": "what does RhoRho like"})
```
> `{'history': [SystemMessage(content='On RhoRho: RhoRho lives in South Korea. RhoRho likes kimchi.')]}`

# Code Sample
---
## Using `PromptTemplate`
```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=120,
    memory_key="chat_history",
)

template = """
    You are a helpful AI talking to a human.

    {chat_history}
    Human:{question}
    You:
"""

chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=PromptTemplate.from_template(template),
    verbose=True,
)

chain.predict(question="My name is RhoRho")
chain.predict(question="I live in Seoul")
chain.predict(question="What is my name?")
```

## Using `ChatPromptTemplate`
- When using `MessagesPalceholder` 
- chat history will automatically added to `system` so that its prompt order does not get mixed

### NOT
```
system: blah
human: a
ai: b
system: summary 
human: c
ai: d
```
### What it will do 
```
system: blah
system: summary 
human: a
ai: b
human: c
ai: d
```

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=50,
    memory_key="chat_history",
    return_messages=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI talking to a human"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

chain = LLMChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True,
)

chain.predict(question="My name is Rho")
chain.predict(question="I live in Seoul")
chain.predict(question="What is my name?")
```

> [!note]
> Entering new LLMChain chain...
> Prompt after formatting: 
> System: You are a helpful AI talking to a human 
> Human: My name is RhoRho 
> 
> > Finished chain. 
> 
> Entering new LLMChain chain... 
> Prompt after formatting: 
> System: You are a helpful AI talking to a human 
> Human: My name is RhoRho AI: Hello RhoRho! How can I assist you today? 
> Human: I live in Seoul 
> > Finished chain. 
> 
> Entering new LLMChain chain... 
> Prompt after formatting: 
> System: You are a helpful AI talking to a human 
> System: RhoRho introduces themselves to the AI and mentions living in Seoul. The AI responds warmly, acknowledging Seoul's vibrant culture and offers assistance with information about the city or South Korea. 
> Human: What is my name? 
> > Finished chain.

> `'Hello! You mentioned your name is RhoRho in your introduction. How can I assist you today?'`

## Using LCEL 
```python 
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=120,
    return_messages=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI talking to a human"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


def load_memory(_):
    return memory.load_memory_variables({})["history"]


chain = RunnablePassthrough.assign(history=load_memory) | prompt | llm


def invoke_chain(question):
    result = chain.invoke({"question": question})
    memory.save_context(
        {"input": question},
        {"output": result.content},
    )
    print(result)

invoke_chain("My name is RhoRho")
invoke_chain("What is my name?")
```
> `content='Hello RhoRho! How can I assist you today?'`
> `content='Your name is RhoRho, as you just told me. How can I help you further, RhoRho?'`
