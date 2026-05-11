from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    MODEL_NAME = os.getenv("MODEL_NAME")

settings = Settings()