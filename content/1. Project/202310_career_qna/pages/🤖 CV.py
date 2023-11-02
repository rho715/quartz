from packages.functions import displayPDF, stream_response, generate_download_link
from packages.common import file_path_cv as file_path
from chains.chain_category import category_chain
from chains.chain_full import full_chain
from chains.chain_search import memory as memory_search
from chains.chain_regular import memory as memory_regular
import streamlit as st
import time
import os

# TODO: prompt Engineering (reply in Korean)
# TODO: Korean mode and English Mode
# TODO: pdf splitting ``

st.set_page_config(layout="wide", page_title="CV", page_icon="🤖")

if st.session_state["authenticated"]:
    col1, col2 = st.columns(spec=[0.65, 0.35], gap="small")

    with col1:
        displayPDF(file_path)
        st.markdown(generate_download_link(file_path, "Yoon Jung Rho Korean_CV.pdf"), unsafe_allow_html=True)

    with col2:
        question = st.text_input(
            "🤖 Ask something about the document",
            placeholder="Can you give me a short summary?",
            # disabled=not uploaded_file,
            # on_change=clear_submit,
        )
        if prompt := question:
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                inputs = {"question": prompt}
                category = category_chain.invoke(inputs)
                st.write("Category: " + category)

                response_generator = stream_response(full_chain, inputs)

                full_response = ""
                message_placeholder = st.empty()

                for ai_answer in response_generator:
                    # Process AI answer content
                    for response in ai_answer["answer"].content.split("\n"):
                        full_response += response + "\n"
                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                        time.sleep(2)

                    # If the category is 'work', append docs to the response
                    if category.lower() == 'work':
                        for doc in ai_answer.get("docs", []):
                            page_content = doc.page_content
                            metadata = doc.metadata
                            source = metadata.get('source', 'N/A')
                            page_num = metadata.get('page', 'N/A')
                            doc_message = f"\n**Source:** {source}\n**Page:** {page_num}\n\n{page_content}"
                            full_response += doc_message + "\n"
                            message_placeholder.markdown(full_response, unsafe_allow_html=True)

                        memory_search.save_context(inputs, {"answer": response})
                    else:
                        memory_regular.save_context(inputs, {"answer": response})

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

