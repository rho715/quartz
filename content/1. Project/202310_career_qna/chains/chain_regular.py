import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from packages.models import CHAT_LLM
from packages.prompts import GENERATE_ANSWER_PROMPT, CONDENSE_QUESTION_PROMPT
from packages.functions import _format_chat_history
from langchain.schema.output_parser import StrOutputParser
from operator import itemgetter
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.memory import ConversationBufferMemory



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

retrieved_question = {
    "question": lambda x: x["standalone_question"]
}

# And finally, we do the part that returns the answers
answer = {
    "answer": retrieved_question | GENERATE_ANSWER_PROMPT | CHAT_LLM,
}
# And now we put it all together!
general_chain = loaded_memory | standalone_question | answer
