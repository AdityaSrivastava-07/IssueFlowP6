"""
Extraction module for IssueFlow (Team RAGA - Problem 6).
Calls local Qwen 2.5 via Ollama over standard HTTP API to extract structured
technical decisions from open-source discussions.
"""

import json
import urllib.error
import urllib.request
from typing import Any, Dict

DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:7b"
MAX_CONTEXT_CHARS = 20000


def extract_decisions(
    discussion_text: str,
    model: str = DEFAULT_MODEL,
    ollama_url: str = DEFAULT_OLLAMA_URL,
) -> Dict[str, Any]:
    """
    Send an engineering discussion thread to local Ollama (Qwen 2.5) and extract decisions.

    Parameters:
        discussion_text (str): Full text of the issue/PR/forum discussion.
        model (str): Ollama model name (default: 'qwen2.5:7b').
        ollama_url (str): Local Ollama HTTP endpoint.

    Returns:
        dict: A dictionary containing a 'decisions' list of structured records.

    Raises:
        RuntimeError: If local Ollama service cannot be reached.
        ValueError: If model response is invalid or missing the required schema.
    """
    # Guard against overflowing the local model's context window
    if len(discussion_text) > MAX_CONTEXT_CHARS:
        print(
            f"-> Notice: Discussion text ({len(discussion_text)} chars) exceeds {MAX_CONTEXT_CHARS}. "
            "Using the final segment for decision extraction..."
        )
        discussion_text = discussion_text[-MAX_CONTEXT_CHARS:]

    prompt = (
        f"Discussion:\n{discussion_text}\n\n"
        "TASK: Extract the key architectural or technical decisions made in the text above. "
        "You are an expert software architect. You MUST respond ONLY with a valid JSON object. "
        "The JSON must follow this EXACT schema and contain a 'decisions' list:\n"
        '{"decisions": [{"decision": "string", "status": "accepted|rejected", "alternative": "string", "reason": "string", "quote": "verbatim quote from text"}]}'
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # Enforce strict JSON output from Ollama
    }

    req = urllib.request.Request(
        ollama_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
            raw_response = result.get("response", "")
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Cannot connect to local Ollama at {ollama_url}. Is 'ollama serve' running? (Details: {e})"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Ollama request failed: {e}") from e

    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        snippet = raw_response[:200]
        raise ValueError(
            f"Model did not return valid JSON. Response snippet: {snippet}..."
        ) from e

    # Contract enforcement & schema normalization
    if "decisions" not in data:
        if isinstance(data, list):
            data = {"decisions": data}
        else:
            raise ValueError("Model output JSON is missing required 'decisions' list key.")

    return data
