from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

router = APIRouter()

from services.ethereum.embedding import train as embedding_train

# --------------- GET ----------------- # 

@router.get(
        "/api/v1/train", 
        response_description="List news related to certain coin",
        responses={404: {"description": "Not found"}}
)
async def train(code: int):
    try:
        if code != 111111:
            raise ValueError("Invalid code")

        news = embedding_train()
        return "Train successfully"

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

