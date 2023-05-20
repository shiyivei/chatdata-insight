
import openai
import os

import sys

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory,"..",".."))
sys.path.insert(0, backend_directory)

# sys.path.insert(0, '/Users/qinjianquan/Career/redstone-network/chatdata-insight/backend')

from core.config import Config
openai.api_key = Config.OPENAI_API_KEY

# print("----root_directory:",backend_directory)
# print("----openai_api_key:",Config.OPENAI_API_KEY)

# openai.api_key = os.environ.get("OPENAI_API_KEY")

COMPLETION_MODEL = "gpt-3.5-turbo"

PROMPT = Config.JUDGEMENT_PROMPT

# print("----prompt:",Config.JUDGEMENT_PROMPT)

# 创建一个函数，名为 get_tour_advice(prompt)
def get_judgment_results0(prompt):
    # 调用 OpenAI API 来生成文本，使用指定的模型和输入文本
    completions = openai.Completion.create (
        engine=COMPLETION_MODEL,
        prompt=prompt,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.0,        
    )
    # 从 API 响应中获取文本输出结果
    message = completions.choices[0].text
    # 返回文本输出结果
    return message



from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

def get_judgment_results(x):
    response_schemas = [
        ResponseSchema(name="case_number", description="case__number is the identification number for potential problem types, of which there are three: 1, 2, 3. If a user is inquiring about information on the blockchain, such as 'What is the balance of address: 0x4bbd2A03A0aD7449EB273f4385cE25E9D2c8D8fE?', it falls under type 1. If the question is about transaction information, like 'What is the price trend of Bitcoin today?', it is type 2. And if it's inquiring about news, such as 'What news are there about Bitcoin?', it is type 3."),
        ResponseSchema(name="question", description="question is the problem itself.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    print("judge result:",result)

    return result

PROMPT = """ You need to obtain the key query parameters based on user input. For example, in the question 'What news are there about Bitcoin?', the key parameter is 'Bitcoin'."""

def get_news_prams(x):

    response_schemas = [
        ResponseSchema(name="token_name", description="token_name represents the query parameters extracted from the user input. For example, in the sentence 'What news are there about Bitcoin?', the query parameter would be 'Bitcoin'.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    print("user request:",x)

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    return result

def get_binance_prams(x):

    response_schemas = [
        ResponseSchema(name="symbol", description="'symbol' represents the query parameters extracted from the user input. For example, in the sentence 'What news are there about Bitcoin?', the query parameter would be 'BTC'."),
        ResponseSchema(name="k_lines", description="'k_lines' stands for K-line intervals, with the default being '15m'. For instance, if a user asks: 'How has Bitcoin performed over the past hour?', then the K-line interval would be '1h'.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = output_parser.get_format_instructions()

    prompt = PromptTemplate(
        template=PROMPT+"\n{format_instructions}\n{question}",
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )

    model = OpenAI(temperature=0)

    _input = prompt.format_prompt(question=x)
    output = model(_input.to_string())
    result = output_parser.parse(output)

    return result