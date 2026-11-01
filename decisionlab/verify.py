"""
Verification engine for IssueFlow (Team RAGA - Problem 6).
Ensures anti-hallucination guarantees by verifying that every extracted decision
quote exists verbatim in the source discussion thread.
"""

import re
from typing import Any, Dict, List


def normalize_text(text: str) -> str:
    """
    Normalize text for robust verbatim matching:
    - Lowercases text
    - Strips code backticks and varied quote characters
    - Collapses consecutive whitespace (spaces, tabs, newlines) into a single space
    """
    if not text:
        return ""
    cleaned = text.lower()
    cleaned = re.sub(r"[`“”\"'‘’]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def is_quote_verified(quote: str, original_text: str) -> bool:
    """
    Return True if normalized quote exists verbatim inside normalized source text.
    Rejects trivial quotes under 10 characters to prevent trivial matching.
    """
    norm_quote = normalize_text(quote)
    norm_source = normalize_text(original_text)

    if len(norm_quote) < 10:
        return False

    return norm_quote in norm_source


def verify_decisions(raw_decisions: Any, original_text: str) -> Dict[str, Any]:
    """
    Filter extracted decision candidates against source discussion.
    Any decision whose quote cannot be verified in the source text is discarded.

    Parameters:
        raw_decisions: Either a dictionary with a 'decisions' list or a list of decision items.
        original_text (str): Full text of the source discussion.

    Returns:
        dict: Verified decisions and summary metrics on hallucinations eliminated.
    """
    verified_decisions: List[Dict[str, Any]] = []
    hallucinations_caught = 0

    # Handle both wrapper dict or direct list
    if isinstance(raw_decisions, dict):
        candidates = raw_decisions.get("decisions", [])
    elif isinstance(raw_decisions, list):
        candidates = raw_decisions
    else:
        candidates = []

    for item in candidates:
        if not isinstance(item, dict):
            hallucinations_caught += 1
            continue

        quote = str(item.get("quote", ""))
        if is_quote_verified(quote, original_text):
            item["verified"] = True
            verified_decisions.append(item)
        else:
            hallucinations_caught += 1

    return {
        "decisions": verified_decisions,
        "verification_stats": {
            "total_extracted": len(candidates),
            "verified_kept": len(verified_decisions),
            "hallucinations_removed": hallucinations_caught,
        },
    }
