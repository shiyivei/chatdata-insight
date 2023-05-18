from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.ethereum.ethereum_info import query_ethereum_info

router = APIRouter()

@router.get(
        "/api/ethereum/info", 
        response_description="List ethereum data",
        responses={404: {"description": "Not found"}}
)
async def get_ethereum_info(
    prompt: str
): 
    try:

        answer = query_ethereum_info(prompt)
        return answer
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
