import streamlit as st
import os
import time
from packages.functions import check_password

st.set_page_config(layout="wide", page_title="Rho's Portfolio", page_icon="👋")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.sidebar.warning('Please enter the username and password')

    username = st.sidebar.text_input("Enter Username")
    password = st.sidebar.text_input("Enter Password", type="password")

    if st.sidebar.button("Login"):
        stored_username = "hi"#st.secrets["general"]["username"]
        stored_password = "hi"#st.secrets["general"]["password"]

        if check_password(stored_password, password) and stored_username == username:
            st.session_state["authenticated"] = True
            st.success("Logged in successfully!")
        else:
            st.sidebar.error("Incorrect Username/Password")

def main():
    st.title("🎉 Welcome to My Professional Portfolio 🎉")

    st.markdown("""
    ## 🚀 Introduction
    This is a platform where you can view my professional resume and CV. 
    Dive deep into my journey, experiences, and achievements!
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🧐 What would you like to explore today?
    - **💖 Resume**: A concise overview of my qualifications, experiences, and skills.
    - **🤖 CV & AI Q&A**: A detailed look into my career, with an interactive AI to answer any of your queries.
    """)

    if st.session_state["authenticated"]:
        st.success("""
        ### 🌈 Have fun exploring other spaces!
        - 🏄‍♀️ [Surfit Resume](https://my.surfit.io/w/283155056)
        - 🐈‍⬛ [Github](https://github.com/rho715)
        - 🤗 [Hugging Face Space](https://huggingface.co/spaces/rho715/private_model) (username: gradio / password: gradio)
        - 🐢 [Blog](https://rho715.github.io/quartz)
        """)

    # Add a playful footer
    st.markdown("<hr/>", unsafe_allow_html=True)

    # ... your existing Streamlit code ...

    # Get the file's last modified timestamp
    file_path = os.path.realpath(__file__)  # Gets the path of the current script (Home.py)
    timestamp = os.path.getmtime(file_path)

    # Convert the timestamp to a human-readable date format
    last_modified_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    # Display the last modified date at the footer
    st.markdown(f'''
    <div style="text-align: right">
        <strong>Last Modified:</strong> {last_modified_date} <br>
        <span style="color: pink">Made with ❤️ and a sprinkle of 🌟</span>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
