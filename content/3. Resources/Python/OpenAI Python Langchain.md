---
title: OpenAI Python Langchain
tags: 
draft: "true"
status:
  - working
---
# [LLMs](https://python.langchain.com/docs/integrations/llms/) vs [Chat Models](https://python.langchain.com/docs/integrations/chat/)

> [!Quote]
> While LLMs are basically “text in — matching text out”, a Chat Model is based on chat messages.
> - from [Models in LangChain](https://lisarebecca.medium.com/models-in-langchain-db04e688ac1f)

- text
	- text-davinchi
- chat
	- gpt-35-turbo

# 목표
- test if you can make chatbot using
	- AzureChatOpenAI
	- BedrockChat
	- ChatGooglePalm

# AzureChatOpenAI
- [ ] AzureChatOpenAI 연결확인
- [ ] ChatHistory 기반으로 대화 가능한지 확인
	- [ ] 히스토리를 프롬프트에 넣는 방법과 (아마 너무 여러가지의 일을 한번에 시키면 못알아들을듯..)
	- [ ] 히스토리를 파라미터로 제공하는 방법
- [ ] Documents 찾는 방법 retriever로 고민해보기 
- [ ] 
https://replit.com/@Yoon-JungJung/ChatGPT#chatmodel_azure.py 