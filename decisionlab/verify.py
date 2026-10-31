import re
from typing import Dict, Any, List

def normalize_text(text: str) -> str:
    """
    Normalize text for strict anti-hallucination matching:
    - Lowercases everything
    - Removes markdown backticks and smart quotes
    - Collapses all newlines, tabs, and multiple spaces into a single space
    """
    if not text:
        return ""
    cleaned = text.lower()
    # Remove backticks and normalize quote characters
    cleaned = re.sub(r"[`“”\"'‘’]", "", cleaned)
    # Collapse any sequence of whitespace/newlines into a single space
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def is_quote_verified(quote: str, original_text: str) -> bool:
    """
    Return True only if the normalized quote exists verbatim inside the normalized original text.
    """
    norm_quote = normalize_text(quote)
    norm_source = normalize_text(original_text)

    # Reject empty or trivially short quotes (less than 10 characters)
    if len(norm_quote) < 10:
        return False

    return norm_quote in norm_source


def verify_decisions(raw_decisions: List[Dict[str, Any]], original_text: str) -> Dict[str, Any]:
    """
    Takes the list returned by extract.py and the raw original discussion text.
    Deletes any decision whose quote cannot be verified in the original text.
    """
    verified_decisions: List[Dict[str, Any]] = []
    hallucinations_caught = 0

    for item in raw_decisions:
        quote = item.get("quote", "")
        if is_quote_verified(quote, original_text):
            item["verified"] = True
            verified_decisions.append(item)
        else:
            hallucinations_caught += 1

    return {
        "decisions": verified_decisions,
        "verification_stats": {
            "total_extracted": len(raw_decisions),
            "verified_kept": len(verified_decisions),
            "hallucinations_removed": hallucinations_caught,
        },
    }


if __name__ == "__main__":
    # Quick local self-test
    sample_source = """
    Guido: We rejected fine-grained locking on every PyDictObject because it causes a 25-30% slowdown.
    Brett: We accepted the --disable-gil build flag for Python/ceval.c.
    """
    
    # Updated to match the exact data contract from your extract.py
    sample_ai_output = [
        {
            "decision": "Fine-grained locking on dicts",
            "status": "rejected",
            "alternative": "",
            "reason": "Causes 25-30% slowdown",
            "quote": "We rejected fine-grained locking on every PyDictObject because it causes a 25-30% slowdown."
        },
        {
            "decision": "Rewrite CPython in Rust",
            "status": "accepted",
            "alternative": "Keep C",
            "reason": "Memory safety",
            "quote": "We have decided to rewrite the entire interpreter in Rust next week."
        }
    ]
    
    result = verify_decisions(sample_ai_output, sample_source)
    print("Verification Result:", result)