import json
import urllib.request
import urllib.error

def extract_decisions(discussion_text):
    # Truncate text if it's too massive for the local 7B context window
    max_chars = 20000
    if len(discussion_text) > max_chars:
        print(f"-> Warning: PR thread is {len(discussion_text)} chars. Truncating to fit context window...")
        discussion_text = discussion_text[-max_chars:]

    # Put the discussion first
    full_prompt = f"Discussion:\n{discussion_text}\n\n"
    
    # Put the strict instructions AT THE VERY END so the model sees them last
    full_prompt += (
        "TASK: Extract the key architectural or technical decisions made in the text above. "
        "You are an expert software architect. You MUST respond ONLY with a valid JSON object. "
        "The JSON must follow this EXACT schema and contain a 'decisions' list: "
        '{"decisions": [{"decision": "string", "status": "string", "alternative": "string", "reason": "string", "quote": "string"}]}'
    )

    # Call local Ollama API
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5:7b",
        "prompt": full_prompt,
        "stream": False,
        "format": "json"  # <-- THIS FORCES OLLAMA TO ONLY OUTPUT VALID JSON
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            raw_response = result.get("response", "")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to local Ollama instance: {e}")
        
    # Safely parse the guaranteed JSON output
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        raise ValueError(f"Model returned invalid JSON format. Raw output: {raw_response[:200]}...")

    # Enforce Data Contract
    if "decisions" not in data:
        # Fallback: if the model returned a list directly instead of the wrapper object
        if isinstance(data, list):
            data = {"decisions": data}
        else:
            raise ValueError("Model JSON is missing a 'decisions' list.")
        
    return data