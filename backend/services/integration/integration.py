
import openai
import os

import sys
import json
from fastapi import HTTPException

import mplfinance as mpf
import pandas as pd

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

# current_directory = os.getcwd()
# print(current_directory)

from core.config import Config
from services.binance import binance_api
from services.news import news_api
from services.onchain_info.airstack_and_quicknode import onchain_info_agent

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
    #     ResponseSchema(name="key_word", description=" 'key_word' represents the query parameters extracted from the user input. For example, in the sentence 'What news are there about Bitcoin?', the 'key_word' would be 'Bitcoin'.")
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



def search_on_internet(question: str) -> str:

    insert_error_data(question, "", "can not find answer")

    os.environ["GOOGLE_CSE_ID"] = "6170c8edfbf634caf"
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDnFWoQElznz9N5frGoVsOuNP55xBBV6zM"


    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name = "Google Search",
        description="Search Google for recent results.",
        func=search.run
    )

    res = tool.run(question)
    
    return res

def analyze_community_activity(input: str) -> str:
    try:
        key_word = get_news_prams(input)
        
    except Exception as e:
        logger.error("ERROR:    Getting news parameters failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    # try:

    #     # print("key word:",key_word)
    #     news = news_api.get_top_headlines("Bitcoin")

    #     print("news:",news)
    # except Exception as e:
    #     logger.error("ERROR:    Getting top headlines from news API failed: %s", str(e))
    #     raise HTTPException(status_code=200, detail=str(e))


    res = "There is no big events about bitcoin in recent days",
    
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


    print("GET BINANCE DATA:",data)
    
    # 将数据转换为DataFrame格式
    df = pd.DataFrame(data)
    # 转换为浮点数
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['quote_asset_volume'] = df['quote_asset_volume'].astype(float)
    df['taker_buy_base_asset_volume'] = df['taker_buy_base_asset_volume'].astype(float)
    df['taker_buy_quote_asset_volume'] = df['taker_buy_quote_asset_volume'].astype(float)

    # 转换为整数
    df['num_trades'] = df['num_trades'].astype(int)
    df['open_time'] = pd.to_datetime(df['open_time'])
    df.set_index('open_time', inplace=True)

    # 绘制蜡烛图
    image_path = 'static/image/candlestick_chart.png'
    mpf.plot(df, type='candle', style='yahoo', volume=True, savefig=image_path)

    # 你需要将下面的 URL 替换成你的应用服务器的地址
    image_url = f'http://137.184.5.217:3005/{image_path}'

    res = {
        "question_type": "binance_data",
        "data": data,
        "image_link": image_url
    }

    print("binance data:",res)

    return



def search_onchain_info(intput: str) -> str:
    try:
        value = onchain_info_agent(intput)

        if value =="Agent stopped due to iteration limit or time limit":
            return "none"

    except Exception as e:
        logger.error("ERROR:    Querying ethereum info failed: %s", str(e))
        raise HTTPException(status_code=200, detail=str(e))

    res = {
        "question_type": "chain_info",
        "data": value,
    }

    return res


def chatdata_agent(origin_question):

    try:
        answer_dict = task_decomposition(origin_question)
    except Exception as e:
        print(f"ERROR:     Error occurred during task decomposition: {e}")
        return None

    try:
        result = result_integration(origin_question,answer_dict)
    except Exception as e:
        print(f"ERROR:     Error occurred during result integration: {e}")
        return None

    print("INFO:     Agent Result:", result)

    return result



# task decomposition

TASK_DECOMPOSITION_PROMPT = "Assume you are a product manager, and you are currently breaking down user's questions into different needs to come up with various answering schemes. Each user's question can be decomposed into up to 5 needs. For example, the question 'List the recent valuable project airdrops and the specific steps to participate in them.' indicates that there are two needs. The first need is 'What are the recent valuable airdrops?', and the second one is 'How to participate in these airdrops?'. However, the question 'Provide me with the most active DApps on the Ethereum blockchain in the past month, along with a summary analysis of their activity' should be decomposed into one question, 'Can you provide me with a list of the most active DApps on the Ethereum blockchain in the past month?'. Even though there is an analysis need, it is based on the result of the first question, which will be solved in the next step, so it does not need to be extracted. Therefore, the core logic is to extract independent questions. Whenever there is a dependency relationship between questions, only the first question needs to be extracted."

DISCRIPTION_PROMPT = "'task_id_1' is the identifier for the first requirement derived from the given question. For instance, if the question is 'List the recent valuable project airdrops and the specific steps to participate in them.', it implies that there are two requirements associated with this question. The first requirement is to determine 'What are the recent valuable airdrop projects?' Thus, 'task_id_1' corresponds to 'What are the recent valuable airdrop projects?' The second requirement pertains to 'How to participate in airdrop projects?' Consequently, 'task_id_2' corresponds to 'How to participate in airdrop projects?' and so on for subsequent requirements.If no further questions can be extracted, 'task_id_x' corresponds to 'none'. For example, in the given question, if only two questions can be extracted, then 'task_id_3', 'task_id_4', 'task_id_5', and so on, would all correspond to 'none'"

def task_decomposition(question):

    response_schemas = [
        ResponseSchema(name="task_id_1", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_2", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_3", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_4", description=DISCRIPTION_PROMPT),
        ResponseSchema(name="task_id_5", description=DISCRIPTION_PROMPT),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=TASK_DECOMPOSITION_PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    _input = prompt.format_prompt(question=question)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("INFO:     DECOMPOSE RESULTS:", result)

    return result


def search_internet_info(input: str) -> str:
    
    return "这是INTERNET上关于LDO的信息"
    

# solution selection

def solution_selection(question: str):


    llm = OpenAI(temperature=0)

    tools = [
        Tool(
            name = "Search something on internet",func=search_on_internet, 
            description="useful for when you need to search for information on the internet."
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

    agent = initialize_agent(tools, llm, agent="zero-shot-react-description",max_iterations=3, verbose=True)
    result = agent.run(question)

    

    print("INFO:     Agent Result:", result)

    return result


# result integration

RESULT_INTEGRATION_PROMPT = "Assume you are a master summarizer. We have broken down the {origin_question} into multiple sub-questions and got the corresponding answers as {ans_dict}. Now, we need you to make a summary for the user based on these answers and the original question."

def result_integration(origin_question,answer_dict):

    if not isinstance(answer_dict, dict):
        print("ERROR:     answer_dict must be a dictionary")
        return None

    if not isinstance(origin_question, str):
        print("ERROR:     origin_question must be a string")
        return None

    ans_dict = {}

    try:
        for key, value in answer_dict.items():
            if value == 'none':
                break
            else:
                print(f'INFO:     Key: {key}, Value: {value}')
                new_key = value
                try:
                    new_value = solution_selection(value)
                except Exception as e:
                    print(f"ERROR:     Error occurred while executing solution_selection: {e}")
                    continue
                ans_dict[new_key] = new_value
    except Exception as e:
        print(f"ERROR:     Error occurred during processing answer_dict: {e}")
        return None

    try:
        multiple_input_prompt = PromptTemplate(
        input_variables=["origin_question", "ans_dict"], 
        template=RESULT_INTEGRATION_PROMPT
        )
    except Exception as e:
        print(f"ERROR:     Error occurred during the creation of PromptTemplate: {e}")
        return None

    try:
        _input=multiple_input_prompt.format(origin_question=origin_question, ans_dict=ans_dict)
    except Exception as e:
        print(f"ERROR:     Error occurred during the formatting of PromptTemplate: {e}")
        return None

    print("INFO:     MULTIPLE INPUT:", _input)

    try:
        model = OpenAI(temperature=0)
    except Exception as e:
        print(f"ERROR:     Error occurred while creating OpenAI model: {e}")
        return None

    try:
        res = model(_input)
    except Exception as e:
        print(f"ERROR:     Error occurred while processing input with the OpenAI model: {e}")
        return None

    return res

ANSWER_JUDGEMENT_PROMPT = "As a language expert, it is your task to assess whether a given response is valid or an exception. A response is deemed invalid if its meaning aligns closely with 'Agent stopped due to iteration limit or time limit.' However, if it deviates from this scenario, the response is classified as valid."

def check_results(x):
    response_schemas = [
        ResponseSchema(name="validity", description="'validity' represents the validity of the answer. When the answer is invalid, the value is 'no'. When the answer is valid, the value is 'yes'."),
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

    print("INFO:   Answer Validity Judge Result:", result)

    return result