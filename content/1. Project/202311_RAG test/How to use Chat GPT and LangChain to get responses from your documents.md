https://mohitdsoni.medium.com/how-to-use-chat-gpt-and-langchain-to-get-responses-from-your-documents-768a9ca0e0d0

```python 
#Import required packages  
#If you have your endpoing then use AzureOpenAI  
#else use  
import openai  
from langchain.llms import AzureOpenAI  
#This will help us create embeddings  
from langchain.embeddings.openai import OpenAIEmbeddings  
#Using ChromaDB as a vector store for the embeddigns  
from langchain.vectorstores import Chroma  
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain.chains import RetrievalQA  
from langchain.document_loaders import DirectoryLoader  
import os  
  
  
os.environ["OPENAI_API_TYPE"] = "azure"  
os.environ["OPENAI_API_VERSION"] = "2022-12-01"  
#Set your API endpoint (API BASE) here if you are using Azure OpenAI  
#If you are using openai common endpoing then you do not need to set this.  
os.environ["OPENAI_API_BASE"] = "OPENAI_API_BASE"  
#Set your OPENAI API KEY here  
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"  
  
  
#Load all the .txt files from docs directory  
loader = DirectoryLoader('./docs/',glob = "**/*.txt")  
docs = loader.load()  
  
  
#Split text into tokens  
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  
texts = text_splitter.split_documents(docs)  
  
  
#Turn the text into embeddings  
embeddings = OpenAIEmbeddings(deployment="NAME_OF_YOUR_MODEL_DEPLOYMENT", chunk_size=1) #This model should be able to generate embeddings. For example, text-embedding-ada-002  
#Store the embeddings into chromadb directory  
docsearch = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory="./chromadb")  
  
  
#Use AzureOpenAI, if you're using a endpoint from Azure Open AI  
llm = AzureOpenAI(deployment_name="NAME_OF_YOUR_MODEL_DEPLOYMENT") #This can be any QnA model. For example, davinci.  
#Use OpenAI if you're using a Azure OpenAI endpoint  
#llm = ChatOpenAI(temperature = 0.7, model_name='MODEL_NAME')  
  
  
qa = RetrievalQA.from_chain_type(llm=llm,  
chain_type="stuff",  
retriever=docsearch.as_retriever(),  
return_source_documents=False  
)  
query = "Where was John born?"  
qa.run(query)
```