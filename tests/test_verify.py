from decisionlab.verify import verify_decisions

def test_verify_decisions_removes_hallucinations():
    sample_text = "We rejected fine-grained locking on every PyDictObject because it causes a 25-30% slowdown."
    
    sample_extracted_data = [
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
            "quote": "This quote is entirely hallucinated and does not exist in the source text."
        }
    ]

    result = verify_decisions(sample_extracted_data, sample_text)
    
    # Assertions to ensure the math and logic hold up
    assert result["verification_stats"]["total_extracted"] == 2
    assert result["verification_stats"]["verified_kept"] == 1
    assert result["verification_stats"]["hallucinations_removed"] == 1
    
    # Ensure only the valid decision remains in the final array
    assert len(result["decisions"]) == 1
    assert result["decisions"][0]["decision"] == "Fine-grained locking on dicts"
    assert result["decisions"][0]["verified"] is True