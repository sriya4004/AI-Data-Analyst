from fastapi import APIRouter

from backend.services.llm_service import generate_response


router = APIRouter()


@router.get("/ask-ai")

def ask_ai(prompt: str):

    response = generate_response(prompt)

    return {
        "prompt": prompt,
        "response": response
    }