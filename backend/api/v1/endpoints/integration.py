
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.news import news_api
from services.binance import binance_api
from datetime import date,timedelta

from services.conversation.integration import get_judgment_results
from services.conversation.integration import get_news_prams
from services.conversation.integration import get_binance_prams
from services.ethereum.ethereum_info import query_ethereum_info
from services.conversation.conversation import stream_output
# from services.ethereum.embedding import train

router = APIRouter()

@router.get(
        "/api/integration/request", 
        response_description="List ethereum data",
        responses={404: {"description": "Not found"}}
)
async def analyze_prompt(
    prompt: str
): 
    try:

        print("user request:",prompt)
        answer = get_judgment_results(prompt)

        if answer["case_number"] == "1":
                 
            value = query_ethereum_info(prompt)

            res = {
            "question_type": "chain_info",
            "data": value,
            }

            return res

        elif answer["case_number"] == "2":
                 
            params = get_binance_prams(prompt)

            symbol = params["symbol"]
            currency="USDT"

            # klines=params["k_lines"]
            klines="1h"

            today = date.today()

            one_day_ago = today - timedelta(days=1)

            dataframe=[one_day_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")]


            print("symbol:",symbol)
            print("currency:",currency)
            print("interval:",klines)
            print("dataframe:",dataframe)

            data = binance_api.get_historical_price(symbol, currency, klines, dataframe)

            res = {
            "question_type": "binance_data",
            "data": data,
            }


            return res

        elif answer["case_number"] == "3":
                 
            params=get_news_prams(prompt)
            news = news_api.get_top_headlines(params["token_name"])

            
            res = {
            "question_type": "news",
            "data": news,
            }

            return res

        else:
            
            print("case_number:",answer["case_number"])
            return "Invalid case_number"  
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})