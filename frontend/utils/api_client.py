from typing import Any, Optional, Tuple

import requests

from utils.config import get_api_base


def _url(path: str) -> str:
    base = get_api_base()
    if not path.startswith("/"):
        path = "/" + path
    return f"{base}{path}"


def health() -> Tuple[bool, dict]:
    try:
        r = requests.get(_url("/health"), timeout=10)
        return r.ok, r.json() if r.content else {}
    except requests.RequestException as e:
        return False, {"error": str(e)}


def upload_file(file_bytes: bytes, filename: str) -> Tuple[bool, Any]:
    try:
        r = requests.post(
            _url("/upload"),
            files={"file": (filename, file_bytes)},
            timeout=120,
        )
        if r.ok:
            return True, r.json()
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return False, {"detail": detail, "status_code": r.status_code}
    except requests.RequestException as e:
        return False, {"error": str(e)}


def list_datasets() -> Tuple[bool, Any]:
    try:
        r = requests.get(_url("/datasets"), timeout=15)
        if r.ok:
            return True, r.json()
        return False, r.text
    except requests.RequestException as e:
        return False, {"error": str(e)}


def generate_insights(dataset_name: str) -> Tuple[bool, Any]:
    try:
        r = requests.get(
            _url("/generate-insights"),
            params={"dataset_name": dataset_name},
            timeout=120,
        )
        if r.ok:
            return True, r.json()
        return False, r.text
    except requests.RequestException as e:
        return False, {"error": str(e)}


def workflow_analysis(dataset_name: str, question: str) -> Tuple[bool, Any]:
    try:
        r = requests.post(
            _url("/workflow-analysis"),
            json={"dataset_name": dataset_name, "question": question},
            timeout=120,
        )
        if r.ok:
            return True, r.json()
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return False, {"detail": detail, "status_code": r.status_code}
    except requests.RequestException as e:
        return False, {"error": str(e)}


def run_agent(
    dataset_name: str,
    question: str,
    date_column: Optional[str] = None,
    target_column: Optional[str] = None,
) -> Tuple[bool, Any]:
    try:
        body: dict = {"dataset_name": dataset_name, "question": question}
        if date_column:
            body["date_column"] = date_column
        if target_column:
            body["target_column"] = target_column
        r = requests.post(_url("/agent"), json=body, timeout=180)
        if r.ok:
            return True, r.json()
        try:
            detail = r.json().get("detail", r.text)
        except Exception:
            detail = r.text
        return False, {"detail": detail, "status_code": r.status_code}
    except requests.RequestException as e:
        return False, {"error": str(e)}
