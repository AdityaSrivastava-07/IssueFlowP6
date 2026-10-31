import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:7b"

PROMPT_HEADER = """Read the developer discussion below and extract the final technical decisions.
Return ONLY a JSON object with a single key "decisions" containing a list.
Each item must have these keys:
- "decision": what was decided, in your own words
- "status": "accepted" or "rejected"
- "alternative": what was considered and not chosen, or "" if none
- "reason": why the choice was made, or "" if not stated
- "quote": copy one sentence word for word exactly as it appears in the discussion text, do not paraphrase

Only include decisions the discussion explicitly states. Do not guess.
If there are no decisions, return {"decisions": []}.

Discussion:
"""


def extract_decisions(discussion_text, model=DEFAULT_MODEL):
    """Send a discussion to the local model and return a list of decision dicts.

    Raises RuntimeError if Ollama is unreachable, and ValueError if the
    model's output is not the expected JSON shape.
    """
    payload = {
        "model": model,
        "prompt": PROMPT_HEADER + discussion_text,
        "format": "json",
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to Ollama at localhost:11434. "
            "Is 'ollama serve' running?"
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}")

    raw = response.json().get("response", "")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON. Raw output: {raw[:200]}")

    decisions = data.get("decisions") if isinstance(data, dict) else None
    if not isinstance(decisions, list):
        raise ValueError("Model JSON is missing a 'decisions' list.")

    cleaned = []
    for d in decisions:
        if not isinstance(d, dict):
            continue
        if isinstance(d.get("status"), str):
            d["status"] = d["status"].strip().lower()
        cleaned.append(d)
    return cleaned


if __name__ == "__main__":
    test_thread = """
    User A: Should we use React or Vue for the new dashboard?
    User B: Let's go with Vue because it is lighter, and React is overkill for this.
    User A: I agree. Vue it is. React is rejected.
    """
    print("Sending text to Qwen (this may take 5 to 10 seconds)...")
    results = extract_decisions(test_thread)
    print(json.dumps(results, indent=2))