from langchain.schema.runnable import RunnableBranch
from chains.chain_search import search_chain
# from chains.chain_search_v2 import search_chain
from chains.chain_regular import general_chain
from chains.chain_category import category_chain

branch = RunnableBranch(
  (lambda x: "work" in x["topic"].lower(), search_chain),
  general_chain
)

full_chain = {
    "topic": category_chain,
    "question": lambda x: x["question"]
} | branch