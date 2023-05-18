import uvicorn
import certifi

from decouple import config
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient



from api.v1.endpoints import openai
from api.v1.endpoints import binance
from api.v1.endpoints import news
from api.v1.endpoints import ethereum
from api.v1.endpoints import conversation
from api.v1.endpoints import integration



DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)



app = FastAPI()

origins = [
    "http://localhost:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL,tlsCAFile=certifi.where())
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Add the routers
app.include_router(openai.router)
app.include_router(binance.router)
app.include_router(news.router)
app.include_router(ethereum.router)
app.include_router(conversation.router)
app.include_router(integration.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=3004)
