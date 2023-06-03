import openai
import sys
import os

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

current_directory = os.path.dirname(os.path.realpath(__file__))
backend_directory = os.path.abspath(os.path.join(current_directory))
sys.path.insert(0, backend_directory)

from core.config import Config
openai.api_key = Config.OPENAI_API_KEY

def train():
        
      print("training...")

      documents = SimpleDirectoryReader('services/ethereum/static/ethereum_schema').load_data()
      index = GPTVectorStoreIndex.from_documents(documents)
      index.storage_context.persist(persist_dir='services/ethereum/static/ethereum_index')

      

