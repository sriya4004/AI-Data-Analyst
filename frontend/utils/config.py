import os

DEFAULT_API_BASE = "http://127.0.0.1:8000"


def get_api_base() -> str:
    return os.getenv("API_BASE_URL", DEFAULT_API_BASE).rstrip("/")
