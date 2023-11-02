import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.schema.output_parser import StrOutputParser

from packages.models import EMBEDDING, CHAT_LLM_4 as CHAT_LLM
from packages.prompts import CONDENSE_QUESTION_PROMPT, ANSWER_PROMPT
from packages.functions import _format_chat_history, _combine_documents
from packages.common import file_path_cv as file_path
from operator import itemgetter
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter

from PyPDF2 import PdfReader

def process_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

text = process_pdf(file_path)
text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            separators=["``"],
            chunk_overlap=0,
        )
chunks = text_splitter.split_text(text)

embeddings = EMBEDDING
docsearch = Chroma.from_documents(chunks, embeddings)
retriever = docsearch.as_retriever()

# First we add a step to load memory
# This adds a "memory" key to the input object
memory = ConversationBufferMemory(return_messages=True, output_key="answer", input_key="question")

loaded_memory = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
)
# Now we calculate the standalone question
standalone_question = {
    "standalone_question": {
        "question": lambda x: x["question"],
        "chat_history": lambda x: _format_chat_history(x['chat_history'])
    } | CONDENSE_QUESTION_PROMPT | CHAT_LLM | StrOutputParser(),
}
# Now we retrieve the documents
retrieved_documents = {
    "docs": itemgetter("standalone_question") | retriever,
    "question": lambda x: x["standalone_question"]
}
# Now we construct the inputs for the final prompt
final_inputs = {
    "context": lambda x: _combine_documents(x["docs"]),
    "question": itemgetter("question")
}
# And finally, we do the part that returns the answers
answer = {
    "answer": final_inputs | ANSWER_PROMPT | CHAT_LLM,
    "docs": itemgetter("docs"),
}
# And now we put it all together!
search_chain = loaded_memory | standalone_question | retrieved_documents | answer


