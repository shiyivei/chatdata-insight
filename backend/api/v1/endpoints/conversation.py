from fastapi import APIRouter
from fastapi.responses import JSONResponse

# import sys
# sys.path.insert(0, '/Users/qinjianquan/Career/redstone-network/chatdata-insight/backend')

from services.conversation.conversation import conversation


router = APIRouter()

@router.get(
        "/api/conversation/request", 
        response_description="List ethereum data",
        responses={404: {"description": "Not found"}}
)
async def get_chatgpt_answer(
    prompt: str
): 
    try:
        
        print("Got prompt",prompt)
        answer = conversation(prompt)

        return answer
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
