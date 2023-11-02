from packages.prompts import DEFAULT_DOCUMENT_PROMPT
from langchain.schema import format_document
import fitz  # PyMuPDF
import streamlit as st
import base64
def _combine_documents(docs, document_prompt = DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)

from typing import Tuple, List
def archive_format_chat_history(chat_history: List[Tuple]) -> str:
    buffer = ""
    for dialogue_turn in chat_history:
        human = "Human: " + dialogue_turn[0]
        ai = "Assistant: " + dialogue_turn[1]
        buffer += "\n" + "\n".join([human, ai])
    return buffer

def _format_chat_history(chat_history) -> str:
  buffer = ""
  for i in range(0, len(chat_history), 2):
    human_msg = chat_history[i]
    ai_msg = chat_history[i+1]

    human = "Human: " + human_msg.content
    ai = "Assistant: " + ai_msg.content
    buffer += "\n" + "\n".join([human, ai])
  return buffer

def stream_response(chain, inputs):
    for segment in chain.stream(inputs):
        yield segment

def displayPDF(file):
    # Open the PDF file
    doc = fitz.open(file)

    zoom = 2.0

    # Iterate through each page
    for i in range(len(doc)):
        page = doc.load_page(i)  # number of page

        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        image_data = pix.tobytes("png")  # Save as PNG format

        # Display each page as an image
        st.image(image_data, use_column_width=True)

def generate_download_link(file, file_name):
    with open(file, "rb") as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()  # encode to base64 (convert bytes to ASCII)
        href = f'<a href="data:file/pdf;base64,{b64}" download="{file_name}">Download PDF</a>'
        return href

def print_green(input):
    # Set the text color to green
    print("\033[32m" + str(input) + "\033[0m", end="")

def print_blue(input):
    # Set the text color to blue
    print("\033[34m" + str(input) + "\033[0m", end="")

def check_password(stored_password, entered_password):
    return stored_password == entered_password


