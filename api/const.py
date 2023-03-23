from dotenv import load_dotenv
import os

load_dotenv()

SERVER = os.getenv("SERVER")
PORT = int(os.getenv("PORT"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
