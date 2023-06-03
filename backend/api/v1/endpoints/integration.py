
from fastapi import APIRouter
from fastapi import HTTPException
from services.integration.integration import chatdata_agent


router = APIRouter()

@router.get(
        "/api/integration/request", 
        response_description="List ethereum data",
        responses={404: {"description": "Not found"}}
)

async def analyze_prompt(prompt: str):
    
    try:
        res = chatdata_agent(prompt)
        return res

    except HTTPException as e:

        # store question and error
        # insert_error_data(prompt,str(e))

        user_message = "We appreciate your question! Sadly, our system isn't able to provide an answer at the moment. Please be assured, we've recorded your query and our committed team is addressing it. As we refine our system, we'll be equipped to answer such questions in the future. We truly value your patience.\n\nWe'd love to invite you to join our lively community at [Website URL]. There, you can help us identify more unanswered questions, or help answer some for the community. As a bonus, you could earn our ecological tokens! Your contribution could greatly impact our services. We'd be thrilled to see you there!"
        
        res = {
                "question_type": "answer_failed",
                "data": user_message,
            }

        return res


        



        


