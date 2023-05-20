import openai

import sys
import os

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory))
sys.path.insert(0, backend_directory)

# sys.path.insert(0, '/Users/qinjianquan/Career/redstone-network/chatdata-insight/backend')

from core.config import Config
openai.api_key = Config.OPENAI_API_KEY
# openai.api_key = os.getenv("OPENAI_API_KEY")

def conversation(prompt):
     
     message = chat_with_gpt(prompt)

     return message

def chat_with_gpt(input):

    prom = """You are an omniscient artificial intelligence, please assist users in solving various problems"""

    conv = Conversation(prom, 20)
    return conv.ask(input) 

# upgrade
class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append({"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                # stream=True,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": message})

        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:21] # Remove the first round conversation left.
        return message
    


from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
)

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def stream_output(prompt):
         
    chat = ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
    return chat([HumanMessage(content=prompt)])

    