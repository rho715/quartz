import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to :rainbow[Rho's] Streamlit Page! 👋")

st.sidebar.success("Select a chatbot above.")

st.markdown(
    """
    ### :blue[Multilingual Language Practice Chatbot App]
    - This Streamlit app is designed to help you practice your language skills in 
        - 🇺🇸 English
        - 🇨🇳 Chinese
        - 🇯🇵 Japanese 
    - It consists of three chatbots, each tailored to a specific language: 
    
    ### 🇺🇸 English Chatbot
    - The English Chatbot is here to assist you in improving your English language skills. You can use it for:
        - Correcting grammar and spelling errors in your sentences.
        - Suggesting more professional words or phrases if you're using slang or casual expressions.
    
    ### 🇨🇳 Chinese Chatbot
    - The Chinese Chatbot is designed to enhance your Chinese language proficiency. It can assist you by:
        - Providing translations of words or phrases into Chinese.
        - Offering pinyin pronunciation guides to help you practice your pronunciation.
    
    ### 🇯🇵 Japanese Chatbot 
    - The Japanese Chatbot is your companion for Japanese language practice. You can use it for:
        - Getting translations of words or phrases into Japanese.
        - Receiving pronunciations and practicing your Japanese pronunciation.
    
    ----------
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a chatbot from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)  

    
"""
)