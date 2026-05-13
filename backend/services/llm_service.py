import google.generativeai as genai
from backend.core.config import settings

if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name=settings.MODEL_NAME or "gemini-1.5-flash"
)

def generate_response(prompt: str):
    """
    Generates a response from the Gemini LLM with a system-level persona.
    """
    full_prompt = f"""
    You are an expert AI Data Analyst. Your job is to analyze datasets, generate 
    insights, explain trends, identify anomalies, and summarize findings clearly.
    Keep responses structured, concise, and insightful.

    User Request:
    {prompt}
    """
    response = model.generate_content(full_prompt)
    return response.text