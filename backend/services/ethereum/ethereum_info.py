import requests
import os
import sys
import logging
import json
import re
from gql import gql,Client
from gql.transport.requests import RequestsHTTPTransport
from llama_index import StorageContext, load_index_from_storage 

# Set up the logger
logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory))
sys.path.insert(0, backend_directory)

from core.config import Config

from services.helpers.chat_models import conversation
from services.helpers.chat_models import stream_output

prompted = False  # Used to determine if ChatGPT has already been prompted

# Define the GraphQL endpoint and API key
quicknode_endpoint = Config.QUICKNODE_ENDPOINT
api_key = Config.QUICKNODE_API_KEY

def query_ethereum_info(request):
    global prompted

    if not prompted:
        init_system_prompt()
        prompted = True

    request_text = "user problem:" + request
    res = ",query result:" + json.dumps(query_pro(request))

    summary = request_text + res
    msg = stream_output(summary)

    return msg


def init_system_prompt():
    prompt = ''' " I want you to be a senior data analyst, language translator. I will give you user problem and query result (json format), you need to use user problem+query result to analyze user needs and give answers. You need to analyze the purpose of user needs: user query needs, you tell the user the query results; user analysis needs, you tell the user the data analysis results. Please reply in the same language as the user problem. If you understand the above requirements, please just reply "ok", please just reply "ok". "'''
    prompt_result = stream_output(prompt)  
    # print("init system.prompt", prompt_result)


def query_pro(prompt):
    message = query_from_pro_model(prompt)
    return message


def query_from_pro_model(prompt):
    graphql_query_sentence = get_graphql_sentence(prompt)

    if graphql_query_sentence is None:
        raise Exception("Failed to get GraphQL sentence")

    response = get_response(graphql_query_sentence)
    if response is None:
        raise Exception("Failed to get response")

    return response


def get_graphql_sentence(prompt):
    try:
        storage_context = StorageContext.from_defaults(persist_dir='./services/ethereum/static/ethereum_index')
        index = load_index_from_storage(storage_context)

        query_engine = index.as_query_engine()

        graphql_query_sentence = query_engine.query(prompt)

        # print("INFO:     GraphQL sentence:", graphql_query_sentence)

        return graphql_query_sentence

    except Exception as e:
        logger.error("ERROR:     Getting GraphQL sentence failed: %s", str(e))
        return None


def get_response(graphql_query_sentence):
    try:
        text = str(graphql_query_sentence)

        query_pattern = r'(query Query\(.*?\)\s*\{[\s\S]*?\}\n\s*)variables'
        variables_pattern = r'variables = (\{[\s\S]*?\})'

        query_match = re.search(query_pattern, text)
        variables_match = re.search(variables_pattern, text)

        if query_match is None:
            logger.error("ERROR:    No query result found, please enter more information.")
            return "No query result found, please enter more information."

        if query_match:
            query_sentence = query_match.group(1)
            print("INFO:     Query Sentence:", query_sentence)

            if variables_match:
                variables = json.loads(variables_match.group(1).replace("'", '"'))
                print("INFO:     Query Variables:", str(variables))

                transport = RequestsHTTPTransport(url=quicknode_endpoint, headers={'x-api-key': api_key}, use_json=True)
                client = Client(transport=transport, fetch_schema_from_transport=True)

                query = gql(query_sentence)

                response = client.execute(query, variable_values=variables)
                print("INFO:     Quick node fetch result:", str(response))

                return response

    except Exception as e:
        logger.error("ERROR:    Getting response failed: %s", str(e))
        return None
