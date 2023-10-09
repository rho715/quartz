# https://www.youtube.com/watch?v=KBo7mZHlink&t=9s

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import openai
import streamlit as st
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common import placeholder_msg, SYSTEM_MESSAGE_ENG, set_gpt3_env, set_gpt4_env
placeholder_msg= placeholder_msg

st.set_page_config(page_title="English Chatbot", page_icon="🇺🇸")
st.markdown("# 🇺🇸 Custom English Chatbot")

with st.expander("🤖 See System Message"):
    st.write(SYSTEM_MESSAGE_ENG)

with st.sidebar:

    option_ai = st.radio(
        "Select AI",
        key="ai",
        options=["GPT3", "GPT4"],
    )

    clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Set up the environment for GPT3 or GPT4
if option_ai == "GPT3":
    set_gpt3_env()
    # openai.api_key = os.getenv("GPT3_OPENAI_API_KEY")
    # openai.api_base = os.getenv("GPT3_OPENAI_API_BASE")
    # openai.api_version = os.getenv("GPT3_OPENAI_API_VERSION")
    # openai.api_type = os.getenv("GPT3_OPENAI_API_TYPE")
    # st.session_state["openai_model"] = "gpt-35-turbo"
else:
    set_gpt4_env()
    # openai.api_key = os.getenv("GPT4_OPENAI_API_KEY")
    # openai.api_base = os.getenv("GPT4_OPENAI_API_BASE")
    # openai.api_version = os.getenv("GPT4_OPENAI_API_VERSION")
    # openai.api_type = os.getenv("GPT4_OPENAI_API_TYPE")
    # st.session_state["openai_model"] = "gpt-4-32k"


SYSTEM_MESSAGE = SYSTEM_MESSAGE_ENG

if "messages_eng" not in st.session_state:
    st.session_state.messages_eng = []

if clear_button:
    st.session_state.messages_eng = []


for message in st.session_state.messages_eng:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(placeholder_msg):
    st.session_state.messages_eng.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        response = openai.ChatCompletion.create(
            engine=st.session_state["openai_model"],
            messages=[{"role": "system", "content": SYSTEM_MESSAGE}] +
                     [
                         {"role": m["role"], "content": m["content"]}
                         for m in st.session_state.messages_eng
                     ],
            # stream=True
        )
        full_response += response.choices[0].message.content
        message_placeholder.markdown(full_response)
    st.session_state.messages_eng.append({"role": "assistant", "content": full_response})

