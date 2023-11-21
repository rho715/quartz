---
title: OpenAI Python
tags:
  - openai
  - python
  - ai
  - streamlit
---



# Simple `ChatCompletion` Code
```python
import os  
import openai  
  
openai.api_key = "{your_key}"  
openai.api_base = "https://{url}.openai.azure.com/"  
openai.api_type = "azure"  
openai.api_version = "2023-03-15-preview"  
  
conversation=[{"role": "system", "content": "You are a helpful assistant."}]  
  
while(True):  
    user_input = input("what do you want to ask: ")        
    conversation.append({"role": "user", "content": user_input})  
  
    response = openai.ChatCompletion.create(  
        engine="gpt-35-turbo", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.  
        messages = conversation  
    )  
  
    conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})  
    print("\n" + response['choices'][0]['message']['content'] + "\n")
```
# Using Streamlit make AI chatbot
## `utils.py`

```python
import openai  
  
def get_initial_message(language="English"):  
    print(language)  
    messages=[  
            {"role":"system","content":f"You are a language AI assistant. \  
            You can help me pratice {language}.\  
            We can do a role-play. So you can pretend to be my friend. \  
            Please do not give me the full dialogue all at once. Give me just once sentence and wait for my resposne. Also if my sentence is grammatically incorrect, please provide better version of my sentence and reply with your answer in parentheses after your response. That way, we are going to take turns. \  
            but if I write something in Korean, that means I do not know how to express my thoughts in {language} so instead of replying me back, please translate my sentence into {language} so that I can copy your translation and ask you the question. \  
            "},  
        ]  
    return messages  
  
def get_chatgpt_response(messages, model="gpt-35-turbo"):  
    print("model: ", model)  
    response = openai.ChatCompletion.create(  
    engine=model,  
    messages=messages  
    )  
    return  response['choices'][0]['message']['content']  
  
def update_chat(messages, role, content):  
    messages.append({"role": role, "content": content})  
    return messages
```


## Sample code

```python
import streamlit as st  
from streamlit_chat import message  
import openai  
from utils import get_initial_message, update_chat, get_chatgpt_response  
  
openai.api_type = ""  
openai.api_key = "" #os.getenv("OPEN_AI_KEY")  
openai.api_base = ""  
openai.api_version = ""  
  
  
st.set_page_config(page_title="Custom ChatGPT", page_icon="💬")  
st.markdown("# Custom ChatGPT")  
st.sidebar.header("Custom ChatGPT")  
  
model = st.selectbox("Select a model", ["gpt-35-turbo", "text-davinci-003"])  
language_selection = st.selectbox("Select a language", ["English", "Japanese", "Chinese"])  
  
#generating 2 empty lists to store past and generated value in the conversation  
  
if 'generated' not in st.session_state:  
    st.session_state['generated'] = []  
if 'past' not in st.session_state:  
    st.session_state['past'] = []  
  
  
query = st.text_input("Query: ", key="input")  
  
if 'messages' not in st.session_state:  
    st.session_state['messages'] = get_initial_message()  
  
if query:  
    with st.spinner("Generating..."):  
        messages = st.session_state['messages']  
        messages = update_chat(messages, "user", query)  
        response = get_chatgpt_response(messages, model=model)  
        messages = update_chat(messages, "assistant", response)  
        st.session_state.past.append(query)  
        st.session_state.generated.append(response)  
  
if st.session_state['generated']:  
  
    for i in range(len(st.session_state['generated'])-1, -1, -1):  
        message(st.session_state['past'][i], avatar_style = 'big-ears', is_user=True, key=str(i) + '_user')  
        message(st.session_state["generated"][i], avatar_style = 'bottts', key=str(i))  
  
with st.expander("Show Messages"):  
    st.write(st.session_state['messages'])  
  
# https://www.youtube.com/watch?v=W7kDwsWFjvE
```