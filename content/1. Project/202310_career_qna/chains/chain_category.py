from packages.prompts import CATEGORY_PROMPT
from packages.models import CHAT_LLM
from langchain.schema.output_parser import StrOutputParser

category_chain = CATEGORY_PROMPT | CHAT_LLM | StrOutputParser()