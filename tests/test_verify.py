from decisionlab.verify import is_quote_verified, normalize_text, verify_decisions


def test_normalize_text():
    raw = "  `Decision`: \"JSON-only\"\n\tfor  v1! "
    expected = "decision: json-only for v1!"
    assert normalize_text(raw) == expected


def test_is_quote_verified_exact_match():
    source = "We decided to keep SQLite solely for unit tests."
    quote = "decided to keep SQLite solely"
    assert is_quote_verified(quote, source) is True


def test_is_quote_verified_short_quote_rejected():
    source = "Yes, we agree."
    quote = "Yes"  # Less than 10 characters
    assert is_quote_verified(quote, source) is False


def test_verify_decisions_removes_hallucinations():
    source_text = (
        "We rejected fine-grained locking on every PyDictObject because it causes a 25-30% slowdown."
    )

    extracted_candidates = [
        {
            "decision": "Fine-grained locking on dicts",
            "status": "rejected",
            "alternative": "Global GIL",
            "reason": "Causes 25-30% slowdown",
            "quote": "We rejected fine-grained locking on every PyDictObject because it causes a 25-30% slowdown.",
        },
        {
            "decision": "Rewrite CPython interpreter in Rust",
            "status": "accepted",
            "alternative": "Keep C",
            "reason": "Memory safety guarantee",
            "quote": "This quote is entirely hallucinated and does not exist in the source discussion.",
        },
    ]

    result = verify_decisions(extracted_candidates, source_text)

    # Verification stats checks
    stats = result["verification_stats"]
    assert stats["total_extracted"] == 2
    assert stats["verified_kept"] == 1
    assert stats["hallucinations_removed"] == 1

    # Only the verified quote must be retained
    decisions = result["decisions"]
    assert len(decisions) == 1
    assert decisions[0]["decision"] == "Fine-grained locking on dicts"
    assert decisions[0]["verified"] is True
