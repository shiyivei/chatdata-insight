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

# extract params from question

JUDGEMENT_PROMPT = '''
Assuming you are an expert in keyword extraction, your task is to extract key terms from user inquiries that will be used to retrieve blockchain-related information.
These keywords are often wallet addresses, ENS domain names, and the like. 
For example, in the question 'can you check the balance of this address 0x60e4d786628fea6478f785a6d7e704777c86a7c6?', the extracted parameter would be '0x60e4d786628fea6478f785a6d7e704777c86a7c6'.
Another question:'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B',the extracted parameter would be '0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B'

'''

def get_query_params(x):
    response_schemas = [
      ResponseSchema(name="question", description="question is the problem itself.for example,'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B.',would be 'Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B.'"),
      ResponseSchema(name="params", description="The parameter extracted from the question, for instance 'can you check the balance of this address 0x60e4d786628fea6478f785a6d7e704777c86a7c6?', would be '0x60e4d786628fea6478f785a6d7e704777c86a7c6'.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=JUDGEMENT_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("INFO:     Judge Result:", result)

    return result


question = "Check the recent transfer records of this account 0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B."
get_query_params(question)