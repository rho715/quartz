from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate

_template_generate_answer = """
Respond to the following question:

Question: {question}
Answer:
"""
GENERATE_ANSWER_PROMPT = PromptTemplate.from_template(_template_generate_answer)



_template_chat_history = """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template_chat_history)

_template_context = """
Answer the question based only on the following context:
{context}

Question: {question}"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(_template_context)

_template_document = """
{page_content}
"""
DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(_template_document)

_template_category = """
Given the user question below, classify it as either being about `work` or `other`.

Do not respond with more than one word.

<question>
{question}
</question>

Classification:
"""
CATEGORY_PROMPT = PromptTemplate.from_template(_template_category)
