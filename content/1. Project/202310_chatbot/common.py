import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import openai
import streamlit as st

placeholder_msg = "Type something in English here!"

SYSTEM_MESSAGE_ENG = """
    Act like as if you are my friend not an AI assistant. After you reply to me, if I wrongly use a word or phrase or if you think my sentence is too casual, please provide your correction in parentheses after your respond to my message.
"""

SYSTEM_MESSAGE_CHI = """
    As Chinese helper,
    reply me back in Chinese. Make sure you provide pinyin.
    Also translate my sentence into Chinese(Traditional) as well. (Don't forget to provide pinyin of the sentence)
"""

SYSTEM_MESSAGE_JPN = """
    As Japanese helper,
    reply me back in Japanese. Make sure you provide its pronunciation.
    Also translate my sentence into Japanese as well. (Don't forget to provide pronunciation of the sentence)
"""

def set_gpt3_env():
    openai.api_key = os.getenv("GPT3_OPENAI_API_KEY")
    openai.api_base = os.getenv("GPT3_OPENAI_API_BASE")
    openai.api_version = os.getenv("GPT3_OPENAI_API_VERSION")
    openai.api_type = os.getenv("GPT3_OPENAI_API_TYPE")
    st.session_state["openai_model"] = "gpt-35-turbo"

def set_gpt4_env():
    openai.api_key = os.getenv("GPT4_OPENAI_API_KEY")
    openai.api_base = os.getenv("GPT4_OPENAI_API_BASE")
    openai.api_version = os.getenv("GPT4_OPENAI_API_VERSION")
    openai.api_type = os.getenv("GPT4_OPENAI_API_TYPE")
    st.session_state["openai_model"] = "gpt-4-32k"
