from fastapi import APIRouter, Response
from fastapi.responses import StreamingResponse
from services.integration.integration import chatdata_agent
from services.helpers.chat_models import stream_output

import base64
import os
import asyncio

router = APIRouter()


@router.get(
    "/api/integration/request", 
    response_description="List ethereum data",
    responses={404: {"description": "Not found"}}
)
def analyze_prompt(prompt: str):
    value = chatdata_agent(prompt)

    image_path = f'static/image/candlestick_chart.png'

    # 获取图片的URL
    base_url = 'http://137.184.5.217:3005/'
    image_url = f'{base_url}{image_path}'

    # 检查文件是否存在
    if os.path.exists(image_path):
        # print("文件存在")
        res = {
            "question_type": "answer",
            "data": value,
            "image_link": image_url
        }
    else:
        res = {
            "question_type": "answer",
            "data": value,
            "image_link": "none"
        }
        # print("文件不存在:",image_path)
    
    return stream_output(str(res))