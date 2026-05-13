from dotenv import load_dotenv
import os
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent
env_path = ROOT_DIR / ".env"

# Load environment variables from the root .env file
load_dotenv(dotenv_path=env_path)

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    MODEL_NAME = os.getenv("MODEL_NAME")

settings = Settings()