from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from main import app

# Data Pydantic model
class Data(BaseModel):
    question: str
    error: Optional[str] = None

# insert data
async def insert_error_data(question: str, error: str):
    collection = app.mongodb["chatadata-insight-collection"]  
    data = Data(question=question, error=error)
    data_dict = data.dict()
    result = await collection.insert_one(data_dict)
    if result:
        return {"status": "data inserted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Insertion failed")


