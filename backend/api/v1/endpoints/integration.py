
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging

from services.news import news_api
from services.binance import binance_api
from datetime import date,timedelta

from services.integration.integration import get_judgment_results
from services.integration.integration import get_news_prams
from services.integration.integration import get_binance_prams
from services.ethereum.ethereum_info import query_ethereum_info
# from services.conversation.conversation import stream_output
# from services.ethereum.embedding import train

router = APIRouter()
# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@router.get(
        "/api/integration/request", 
        response_description="List ethereum data",
        responses={404: {"description": "Not found"}}
)

async def analyze_prompt(prompt: str):
    
    try:
        try:
            answer = get_judgment_results(prompt)
        except Exception as e:
            logger.error("ERROR:    Getting judgment results failed: %s", str(e))
            raise HTTPException(status_code=200, detail=str(e))

        if answer["case_number"] == 1 or answer["case_number"] == "1":
            try:
                value = query_ethereum_info(prompt)
            except Exception as e:
                logger.error("ERROR:    Querying ethereum info failed: %s", str(e))
                raise HTTPException(status_code=200, detail=str(e))

            res = {
                "question_type": "chain_info",
                "data": value,
            }
            return res

        elif answer["case_number"] == 2 or answer["case_number"] == "2":
            try:
                params = get_binance_prams(prompt)
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

            return res

        elif answer["case_number"] == 3 or answer["case_number"] == "3":
            try:
                params = get_news_prams(prompt)
            except Exception as e:
                logger.error("ERROR:    Getting news parameters failed: %s", str(e))
                raise HTTPException(status_code=200, detail=str(e))

            try:
                news = news_api.get_top_headlines(params["key_word"])
            except Exception as e:
                logger.error("ERROR:    Getting top headlines from news API failed: %s", str(e))
                raise HTTPException(status_code=200, detail=str(e))

            res = {
                "question_type": "news",
                "data": news,
            }

            return res

        else:
            print("wrong case_number:", answer["case_number"])
            raise HTTPException(status_code=200, detail="Invalid case_number")

    except HTTPException as e:
        user_message = "We appreciate your question! Sadly, our system isn't able to provide an answer at the moment. Please be assured, we've recorded your query and our committed team is addressing it. As we refine our system, we'll be equipped to answer such questions in the future. We truly value your patience.\n\nWe'd love to invite you to join our lively community at [Website URL]. There, you can help us identify more unanswered questions, or help answer some for the community. As a bonus, you could earn our ecological tokens! Your contribution could greatly impact our services. We'd be thrilled to see you there!"
        
        res = {
                "question_type": "answer_failed",
                "data": user_message,
            }

        return res
        