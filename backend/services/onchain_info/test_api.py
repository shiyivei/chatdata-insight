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

import mplfinance as mpf
import pandas as pd
import json


def save_data_pic():

    data_string ='''

    {'question_type': 'binance_data', 'data': [{'open_time': Timestamp('2023-06-10 08:00:00'), 'close_time': Timestamp('2023-06-10 09:59:59.999000'), 'open': '25647.69000000', 'high': '25647.69000000', 'low': '25571.37000000', 'close': '25598.15000000', 'volume': '0.70444000', 'quote_asset_volume': '18035.64091760', 'num_trades': 143, 'taker_buy_base_asset_volume': '0.31279000', 'taker_buy_quote_asset_volume': '8006.52613930', 'ignore': '0', 'open_timestamp': 1686384000000, 'close_timestamp': 1686391199999}, {'open_time': Timestamp('2023-06-10 06:00:00'), 'close_time': Timestamp('2023-06-10 07:59:59.999000'), 'open': '25588.56000000', 'high': '25766.95000000', 'low': '25551.40000000', 'close': '25639.55000000', 'volume': '13.63376000', 'quote_asset_volume': '349727.37814790', 'num_trades': 1999, 'taker_buy_base_asset_volume': '5.83452000', 'taker_buy_quote_asset_volume': '149777.46830890', 'ignore': '0', 'open_timestamp': 1686376800000, 'close_timestamp': 1686383999999}, {'open_time': Timestamp('2023-06-10 04:00:00'), 'close_time': Timestamp('2023-06-10 05:59:59.999000'), 'open': '26344.42000000', 'high': '26368.27000000', 'low': '25577.01000000', 'close': '25584.93000000', 'volume': '32.02025000', 'quote_asset_volume': '828196.17963380', 'num_trades': 3262, 'taker_buy_base_asset_volume': '12.97894000', 'taker_buy_quote_asset_volume': '335673.18458880', 'ignore': '0', 'open_timestamp': 1686369600000, 'close_timestamp': 1686376799999}, {'open_time': Timestamp('2023-06-10 02:00:00'), 'close_time': Timestamp('2023-06-10 03:59:59.999000'), 'open': '26402.06000000', 'high': '26443.73000000', 'low': '26305.90000000', 'close': '26344.49000000', 'volume': '20.26554000', 'quote_asset_volume': '534258.59995870', 'num_trades': 1724, 'taker_buy_base_asset_volume': '9.32649000', 'taker_buy_quote_asset_volume': '246072.20652700', 'ignore': '0', 'open_timestamp': 1686362400000, 'close_timestamp': 1686369599999}, {'open_time': Timestamp('2023-06-10 00:00:00'), 'close_time': Timestamp('2023-06-10 01:59:59.999000'), 'open': '26505.11000000', 'high': '26544.00000000', 'low': '26320.00000000', 'close': '26402.06000000', 'volume': '24.45100000', 'quote_asset_volume': '645802.85377840', 'num_trades': 1207, 'taker_buy_base_asset_volume': '7.06325000', 'taker_buy_quote_asset_volume': '186984.39938760', 'ignore': '0', 'open_timestamp': 1686355200000, 'close_timestamp': 1686362399999}, {'open_time': Timestamp('2023-06-09 22:00:00'), 'close_time': Timestamp('2023-06-09 23:59:59.999000'), 'open': '26474.20000000', 'high': '26521.13000000', 'low': '26452.23000000', 'close': '26504.97000000', 'volume': '15.21303000', 'quote_asset_volume': '402816.16576860', 'num_trades': 1229, 'taker_buy_base_asset_volume': '11.70959000', 'taker_buy_quote_asset_volume': '310065.03729690', 'ignore': '0', 'open_timestamp': 1686348000000, 'close_timestamp': 1686355199999}, {'open_time': Timestamp('2023-06-09 20:00:00'), 'close_time': Timestamp('2023-06-09 21:59:59.999000'), 'open': '26438.88000000', 'high': '26514.87000000', 'low': '26414.35000000', 'close': '26463.44000000', 'volume': '22.15833000', 'quote_asset_volume': '586590.72882450', 'num_trades': 1814, 'taker_buy_base_asset_volume': '12.92921000', 'taker_buy_quote_asset_volume': '342252.92602580', 'ignore': '0', 'open_timestamp': 1686340800000, 'close_timestamp': 1686347999999}, {'open_time': Timestamp('2023-06-09 18:00:00'), 'close_time': Timestamp('2023-06-09 19:59:59.999000'), 'open': '26495.41000000', 'high': '26570.00000000', 'low': '26400.00000000', 'close': '26413.76000000', 'volume': '41.39761000', 'quote_asset_volume': '1096699.52863550', 'num_trades': 1853, 'taker_buy_base_asset_volume': '21.05120000', 'taker_buy_quote_asset_volume': '558086.19343550', 'ignore': '0', 'open_timestamp': 1686333600000, 'close_timestamp': 1686340799999}, {'open_time': Timestamp('2023-06-09 16:00:00'), 'close_time': Timestamp('2023-06-09 17:59:59.999000'), 'open': '26475.84000000', 'high': '26565.30000000', 'low': '26435.03000000', 'close': '26495.41000000', 'volume': '15.79703000', 'quote_asset_volume': '418640.52493790', 'num_trades': 1426, 'taker_buy_base_asset_volume': '11.67278000', 'taker_buy_quote_asset_volume': '309486.99301750', 'ignore': '0', 'open_timestamp': 1686326400000, 'close_timestamp': 1686333599999}, {'open_time': Timestamp('2023-06-09 14:00:00'), 'close_time': Timestamp('2023-06-09 15:59:59.999000'), 'open': '26649.97000000', 'high': '26700.00000000', 'low': '26470.43000000', 'close': '26515.44000000', 'volume': '26.94224000', 'quote_asset_volume': '717162.28307350', 'num_trades': 1684, 'taker_buy_base_asset_volume': '16.58819000', 'taker_buy_quote_asset_volume': '441945.46909970', 'ignore': '0', 'open_timestamp': 1686319200000, 'close_timestamp': 1686326399999}, {'open_time': Timestamp('2023-06-09 12:00:00'), 'close_time': Timestamp('2023-06-09 13:59:59.999000'), 'open': '26623.58000000', 'high': '26762.26000000', 'low': '26598.98000000', 'close': '26647.92000000', 'volume': '22.98227000', 'quote_asset_volume': '612803.31251090', 'num_trades': 1256, 'taker_buy_base_asset_volume': '16.48332000', 'taker_buy_quote_asset_volume': '439525.95090990', 'ignore': '0', 'open_timestamp': 1686312000000, 'close_timestamp': 1686319199999}, {'open_time': Timestamp('2023-06-09 10:00:00'), 'close_time': Timestamp('2023-06-09 11:59:59.999000'), 'open': '26614.51000000', 'high': '26653.70000000', 'low': '26402.06000000', 'close': '26623.58000000', 'volume': '10.62624000', 'quote_asset_volume': '282520.55055830', 'num_trades': 905, 'taker_buy_base_asset_volume': '4.21881000', 'taker_buy_quote_asset_volume': '112280.16311280', 'ignore': '0', 'open_timestamp': 1686304800000, 'close_timestamp': 1686311999999}], 'image_link': ''}

    '''

    data_string=data_string.replace("'", '"')

    data = json.loads(data_string)

    # 将数据转换为DataFrame格式
    df = pd.DataFrame(data)
    df['open_time'] = pd.to_datetime(df['open_time'])
    df.set_index('open_time', inplace=True)

    # 绘制蜡烛图
    mpf.plot(df, type='candle', style='yahoo', volume=True, savefig='/backend/statics/image/candlestick_chart.png')

    print("data:",df)


save_data_pic()