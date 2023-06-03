
import openai
import os

import sys
from fastapi import HTTPException

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

from core.config import Config
from services.binance import binance_api
from services.news import news_api
from services.ethereum.ethereum_info import query_ethereum_info

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

JUDGEMENT_PROMPT = Config.JUDGEMENT_PROMPT

def get_judgment_results(x):
    response_schemas = [
        ResponseSchema(name="case_number", description="case__number is the identification number for potential problem types, of which there are three: 1, 2, 3. If a user is inquiring about information on the blockchain, such as 'What is the balance of address: 0x4bbd2A03A0aD7449EB273f4385cE25E9D2c8D8fE?', it falls under type 1. If the question is about transaction information, like 'What is the price trend of Bitcoin today?', it is type 2. And if it's inquiring about news, such as 'What news are there about Bitcoin?', it is type 3."),
        ResponseSchema(name="question", description="question is the problem itself.")
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

NEWS_PROMPT = Config.NEWS_PROMPT

# print("news prompt:",NEWS_PROMPT)

def get_news_prams(x):

    # response_schemas = [
    #     ResponseSchema(name="key_word", description="key_word represents the query parameters extracted from the user input. For example, in the sentence 'What news are there about Bitcoin?', the query parameter would be 'Bitcoin'.")
    # ]
    # output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    # format_instructions = output_parser.get_format_instructions()

    # prompt = PromptTemplate(
    #     template=NEWS_PROMPT+"\n{format_instructions}\n{question}",
    #     input_variables=["question"],
    #     partial_variables={"format_instructions": format_instructions}
    # )

    # model = OpenAI(temperature=0)

    # _input = prompt.format_prompt(question=x)
    # output = model(_input.to_string())
    # result = output_parser.parse(output)

    # print("INFO:     News prams:", result)

    return x

BINANCE_PROMPT = Config.BINANCE_PROMPT

def get_binance_prams(x):

    response_schemas = [
        ResponseSchema(name="symbol", description="'symbol' represents the query parameters extracted from the user input. For example, in the sentence 'What news are there about Bitcoin?', the query parameter would be 'BTC'."),
        ResponseSchema(name="k_lines", description="'k_lines' stands for K-line intervals, with the default being '1h'. Here are some examples, 'Last week': '1d'.'Last month': '1d'.'Yesterday': '1h'.'In 3 hours': '5m'.'Last hours': '5m'.'Two years ago': '3d'.If there is no time information, please provide '1h' as the answer. Please only provide the answer of the interval in the required format, don't explain anything."),
        ResponseSchema(name="dataframe", description="'dataframe' stands Extract time info from the provided text and translate to a time interval [start, end], expressed using python module `datetime.datetime.now()` and `datetime.timedelta()`. Here are some examples, 'Last week': '[datetime.datetime.now() - datetime.timedelta(weeks=1), datetime.datetime.now()]'.'Last month': '[datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()]'.'Yesterday': '[datetime.datetime.now() - datetime.timedelta(days=1), datetime.datetime.now()]'.'In 3 hours': '[datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=3)]'.'Two years ago': '[datetime.datetime.now() - datetime.timedelta(days=730), datetime.datetime.now()]'.If there is no time information, please provide '[]' as the answer. Please only provide the answer of the interval in the required format, don't explain anything."),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=BINANCE_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("INFO:     BINANCE PRAMS:", result)

    return result



def search_team_info(input: str) -> str:
    return "LDO背后是个大团队"

def analyze_community_activity(input: str) -> str:
    try:
        key_word = get_news_prams(input)
    except Exception as e:
        logger.error("ERROR:    Getting news parameters failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    # try:
    #     news = news_api.get_top_headlines(key_word)
    # except Exception as e:
    #     logger.error("ERROR:    Getting top headlines from news API failed: %s", str(e))
    #     raise HTTPException(status_code=200, detail=str(e))

    res = {
        "question_type": "news",
        "data": "There is no big events about bitcoin in recent days",
    }

    return res

def analyze_solved_needs(intput: str) -> str:
    return "LDO是一个去中心化的金融产品"  

def search_token_distribution(intput: str) -> str:
    return "现在80%的代币都被社区持有"

def search_inovation(intput: str) -> str:
    return "它是一个杠杆金融产品"

def search_economy_model(intput: str) -> str:
    return "一部分代币空投给社区，一部分给投资人"

def search_roadmap_and_historical_events(intput: str) -> str:
    return "LDO 最近张的很凶"

def search_price_info(intput: str) -> str:
    try:
        params = get_binance_prams(intput)
    except Exception as e:
        logger.error("ERROR:    Getting Binance parameters failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    symbol = params["symbol"]
    currency = "USDT"
    klines = params["k_lines"]
    dataframe = params["dataframe"]

    print("symbol:", symbol)
    print("currency:", currency)
    print("klines:", klines)
    print("dataframe:", dataframe)
    
    try:
        data = binance_api.get_historical_price(symbol, currency, klines, dataframe)
    except Exception as e:
        logger.error("ERROR:    Getting historical price from Binance failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    res = {
        "question_type": "binance_data",
        "data": data,
    }


    print("binance data:",res)

    return res



def search_onchain_info(intput: str) -> str:
    try:
        value = query_ethereum_info(intput)
    except Exception as e:
        logger.error("ERROR:    Querying ethereum info failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    res = {
        "question_type": "chain_info",
        "data": value,
    }

    return res


def chatdata_agent(question):

    from langchain.agents import initialize_agent, Tool
    from langchain.llms import OpenAI

    llm = OpenAI(temperature=0)


    tools = [
        Tool(
            name = "Search for startup team information",func=search_team_info, 
            description="useful for when you need to answer questions about the founders or startup team information of a project"
        ),
        Tool(name="Analyze community activity", func=analyze_community_activity, 
            description="useful for when you need to answer questions about the community activity or social media activity of a specific project"
        ),
        Tool(name="Core selling points of the project", func=analyze_solved_needs, 
            description="useful for when you need to answer questions about what user needs a specific project actually addresses"
        ),

        Tool(name="Token distribution", func=search_token_distribution, 
            description="useful for when you need to answer questions about the token distribution of a specific project, such as the current token lock-up amount, release schedule, concentration of holdings, and so on"
        ),

        Tool(name="Project innovations", func=search_inovation, 
            description="useful for when you need to answer questions about the innovations of a specific project, such as innovations in the technical solution or innovations in the business model"
        ),
        
        Tool(name="Project's economic model", func=search_economy_model, 
            description="useful for when you need to answer questions about the economic model of a specific project, such as the participants involved in the economic model, how the economic model incentivizes participants, and the token minting or burning mechanisms, among others"
        ),

        Tool(name="Project's roadmap and historical events", func=search_roadmap_and_historical_events, 
            description="useful for when you need to answer questions about the roadmap or significant events of a specific project, such as when certain upgrades were completed, new features were developed, or major security incidents occurred, among others"
        ),  

        Tool(name="Token price", func=search_price_info, 
            description="useful for  when you need to answer questions about the token price of a specific project, such as price trends, high and low points in the price, and so on"
        ),

        Tool(name="Onchain information", func= search_onchain_info, 
            description="useful for when you need to answer questions about certain on-chain information, such as contract information, address information, or transaction information, among others"
        ),
    ]

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    result = agent.run(question)

    print("INFO:     Agent Result:", result)

    return result