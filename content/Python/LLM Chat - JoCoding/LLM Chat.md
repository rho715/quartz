---
title: 랭체인(LangChain) 이용한 AI 웹서비스 만들기 (with ChatGPT, LLaMA 2)
tags:
  - ai
  - python
  - streamlit
  - chatbot
  - langchain
draft:
---

# 전체  구조 & 순서

![[Pasted image 20231010201844.png]]

1. Loader를 사용해서 pdf 로딩
2. PDF 쪼개기 -> 검색 용이
3. Embedding 만들기 -> DB에 저장
4. Chroma 사용
5. Vector DB: 벡터 저장에 특화된 DB
6. Pinecone vs Chroma
	- pinecone: Saas
	- Chroma: 그냥 로컬에서 사용가능
7. Embedding: Text, Image, Video → Vector Data 로 바꿔주는
	- 비슷하게 생긴애들 근처에 모임
	-  [Visualizing MNIST: An Exploration of Dimensionality Reduction - colah's blog](https://colah.github.io/posts/2014-10-Visualizing-MNIST/)
        - [꼬맨틀 - 단어 유사도 추측 게임 - 뉴스젤리 : 데이터 시각화 전문 기업](https://semantle-ko.newsjel.ly/)


# [Codes](https://github.com/rho715/quartz/tree/v4/content/3.%20Resources/Python/LLM%20Chat%20-%20JoCoding)
1. LLM Chat - Local Code
2. LLM Chat - Streamlit
3. LLM Chat - Buy me a coffee
4. LLM Chat - Streaming

# File
> [!abstract]- PDF
> [[[조코딩]랭체인 AI 웹서비스 만들기_compressed.pdf]]