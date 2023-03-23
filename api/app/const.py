from dotenv import load_dotenv
import os

load_dotenv()

SERVER_QDRANT = os.getenv("SERVER_QDRANT")
PORT_QDRANT = int(os.getenv("PORT_QDRANT"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
