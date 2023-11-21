---
title: LangChain Expression Language (LCEL)
tags:
  - ai
  - langchain
  - python
---
# Why use LCEL
[link](https://python.langchain.com/docs/expression_language/why)
1. Supports putting prototypes into production with no code changes
2. Supports streaming for low latency
3. Supports both synchronous and asynchronous usage
4. Supports optimized parallel execution
5. Supports retries and fallbacks for reliability 

# What you can do 
- [streaming](https://python.langchain.com/docs/expression_language/interface#stream)
- [Invoke](https://python.langchain.com/docs/expression_language/interface#invoke)
- [Batch](https://python.langchain.com/docs/expression_language/interface#batch)
	- throw multiple inputs (ie. `chain.batch([{"topic":"bears"}, {"topic":"cats"}])`)
- [`Runnable.bind()`](https://python.langchain.com/docs/expression_language/how_to/binding)
	- pass in args (ie. `model.bind(stop="SOLUTION")`)
- [Configuration](https://python.langchain.com/docs/expression_language/how_to/configure#configuration-fields)
	- can configure parameters like temperature
	```python
	from langchain.chat_models import ChatOpenAI
	from langchain.prompts import PromptTemplate
	
	model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
	    )
	)
	```
- [Configuration with alternatives](https://python.langchain.com/docs/expression_language/how_to/configure#with-prompts-and-llms)
	- you can easily switch between prompts & llm models 
		- write a poem using gpt-4
		- tell me a joke using gpt-4
		- write a poem using claude
		- tell me a joke using claude 
- Flexible Fallbacks design
- [Define functions and run them with AI](https://python.langchain.com/docs/expression_language/how_to/functions)
	- ie. What is total length of a + b 
	- {"a": "aloha", "b": "hawaii"}
- [llm chain 결과로 나온 strings -> List로 변환](https://python.langchain.com/docs/expression_language/how_to/generators)
- [llm chain 병렬 처리 (you can get joke & poem at the same time)](https://python.langchain.com/docs/expression_language/how_to/map)
- [category에 따른 llm chain branch 처리도 가능](https://python.langchain.com/docs/expression_language/how_to/routing)
# 질문
- What's Async
- [Attaching OpenAI Functions usage](https://python.langchain.com/docs/expression_language/how_to/binding#attaching-openai-functions)
- 