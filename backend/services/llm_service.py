import google.generativeai as genai
import os
from dotenv import load_dotenv

from backend.core.config import settings

# Configure Gemini API using settings
if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

# Load model using settings
model = genai.GenerativeModel(
    model_name=settings.MODEL_NAME or "gemini-1.5-flash"
)

def generate_response(prompt: str):

    full_prompt = f"""
    You are an expert AI Data Analyst.

    Your job is to:
    - analyze datasets
    - generate business insights
    - explain trends
    - identify anomalies
    - summarize findings clearly

    Keep responses:
    - structured
    - concise
    - insightful

    User Dataset Analysis Request:
    {prompt}
    """

    response = model.generate_content(full_prompt)

    return response.text