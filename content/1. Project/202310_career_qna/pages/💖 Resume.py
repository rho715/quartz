from packages.common import file_path_resume, file_path_resume_eng
from packages.functions import displayPDF, generate_download_link,check_password
import streamlit as st
import os
import time

st.set_page_config(layout="wide", page_title="Resume", page_icon="💖")


if st.session_state["authenticated"]:
    col1, col2 = st.columns(spec=[0.5, 0.5], gap="small")
    with col1:
        st.write("국문 이력서")
        displayPDF(file_path_resume)
        st.markdown(generate_download_link(file_path_resume, "Korean_Resume.pdf"), unsafe_allow_html=True)
    with col2:
        st.write("영문 이력서")
        displayPDF(file_path_resume_eng)
        st.markdown(generate_download_link(file_path_resume_eng, "English_Resume.pdf"), unsafe_allow_html=True)

else:
    st.warning('Please enter the username and password')

file_path = os.path.realpath(__file__)  # Gets the path of the current script (Home.py)
timestamp = os.path.getmtime(file_path)

# Convert the timestamp to a human-readable date format
last_modified_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

# Display the last modified date at the footer
st.markdown(f'''
<div style="text-align: right">
    <span style="color: pink"> <strong>Last Modified:</strong> {last_modified_date} </span>
</div>
''', unsafe_allow_html=True)
