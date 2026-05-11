from openai import OpenAI

from backend.core.config import settings


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY
)


def generate_response(prompt: str):

    completion = client.chat.completions.create(
    model=settings.MODEL_NAME,
    messages=[
        {
            "role": "system",
            "content": """
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
            """
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    max_tokens=700,
    temperature=0.3
    )

    return completion.choices[0].message.content