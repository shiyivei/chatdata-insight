import json
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import re

import os
import sys


current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory))
sys.path.insert(0, backend_directory)

from core.config import Config

from services.conversation.conversation import conversation
from services.conversation.conversation import stream_output

prompted = False  # Used to determine if ChatGPT has already been prompted

def query_ethereum_info(request):
   
    global prompted

    if not prompted:
        init_system_prompt()
        prompted = True


    request_text = "user problem:" + request
    res = ",query result:" + json.dumps(query_pro(request))

    summary = request_text + res
    # msg = conversation(summary) # no stream output
    msg = stream_output(summary)

    return msg

def init_system_prompt():
    # Initialize the system prompt to inform ChatGPT of the task requirements
    prompt = ''' " I want you to be a senior data analyst, language translator. I will give you user problem and query result (json format), you need to use user problem+query result to analyze user needs and give answers. You need to analyze the purpose of user needs: user query needs, you tell the user the query results; user analysis needs, you tell the user the data analysis results. Please reply in the same language as the user problem. If you understand the above requirements, please just reply "ok", please just reply "ok". "'''
    # prompt_result = conversation(prompt)  # no stream output
    prompt_result = stream_output(prompt)  

    print("init system.prompt", prompt_result)

def query_pro(prompt):
    # Query the professional model with the given prompt
    message = query_from_pro_model(prompt)
    return message


def query_from_pro_model(prompt):

     # get graphql query sentence

     graphql_query_sentence = get_graphql_sentence(prompt)

     # get response from graphql query
     response = get_response(graphql_query_sentence)
     return response

from llama_index import StorageContext, load_index_from_storage  

def get_graphql_sentence(prompt):
         try:
               # rebuild storage context
               storage_context = StorageContext.from_defaults(persist_dir='./services/ethereum/static/ethereum_index')
               # load index
               index = load_index_from_storage(storage_context)

               query_engine = index.as_query_engine()

               # produce graphql sentence
               graphql_query_sentence = query_engine.query(prompt)

               print("get graphql sentence:",graphql_query_sentence)

               return graphql_query_sentence

         except Exception as e:
               print(f"An error occurred: {e}")
               return None


# Define the GraphQL endpoint and API key
quicknode_endpoint = Config.QUICKNODE_ENDPOINT
api_key = Config.QUICKNODE_API_KEY


def get_response(graphql_query_sentence):
    try:
        text = str(graphql_query_sentence)

        query_pattern = r'(query Query\(.*?\)\s*\{[\s\S]*?\}\n\s*)variables'
        variables_pattern = r'variables = (\{[\s\S]*?\})'

        query_match = re.search(query_pattern, text)
        variables_match = re.search(variables_pattern, text)

        if query_match is None:
            return "No query result found, please enter more information."

        if query_match:
            query_sentence = query_match.group(1)
            print("Query:",query_sentence)

            if variables_match:
                variables = json.loads(variables_match.group(1).replace("'", '"'))
                print("Variables:",variables)

                # Set up the GraphQL client
                transport = RequestsHTTPTransport(url=quicknode_endpoint, headers={'x-api-key': api_key}, use_json=True)
                client = Client(transport=transport, fetch_schema_from_transport=True)

                query = gql(query_sentence)

                # Execute the query and print the result
                response = client.execute(query, variable_values=variables)
                print(" quick node fetch result :",response)

                return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



