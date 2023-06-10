import requests
import openai
import os

import sys
import json
from fastapi import HTTPException

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

from core.config import Config


os.environ["OPENAI_API_KEY"] = Config.OPENAI_API_KEY

COMPLETION_MODEL = "gpt-3.5-turbo"

import logging
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities import GoogleSearchAPIWrapper

# extract params from question

JUDGEMENT_PROMPT = '''
Assuming you are an expert in keyword extraction, your task is to extract key terms from user inquiries that will be used to retrieve blockchain-related information.
These keywords are often wallet addresses, ENS domain names, and the like. 
For example, in the question 'can you check the balance of this address 0x60e4d786628fea6478f785a6d7e704777c86a7c6?', the extracted parameter would be '0x60e4d786628fea6478f785a6d7e704777c86a7c6'.
Another question:'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B',the extracted parameter would be '0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'

'''

def test_openai_api():
    
    llm = OpenAI(temperature=0)

    text = f""" The kitten and the puppy are good friends.\
    They often play, explore, and enjoy beautiful moments together.\
    Every day, they chase butterflies and leap on the green grass.\
    The kitten teaches the puppy how to catch mice, while the puppy leads the kitten to explore the forest.\
    They help and care for each other.\
    Whether it's sunny or rainy, they are always together.\
    People are often touched by the deep friendship between them.\
    The story of the kitten and the puppy is a wonderful melody about friendship and cooperation, echoing in our hearts forever.
    """

    prompt = f"""
    Summarize the text delimited by triple backtricks \ 
    into a single sentence.
    ```{text}```
    """


    print("INFO:     Judge Result:", llm(prompt))


# test_openai_api()

def search_on_internet(question: str) -> str:

    os.environ["GOOGLE_CSE_ID"] = "6170c8edfbf634caf"
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDnFWoQElznz9N5frGoVsOuNP55xBBV6zM"


    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name = "Google Search",
        description="Search Google for recent results.",
        func=search.run
    )

    res = tool.run(question)

    print("search results:",res)
    
    return res


# search_on_internet("Bitcoin")