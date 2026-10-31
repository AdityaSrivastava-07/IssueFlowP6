import argparse
import json
from pathlib import Path

# Corrected imports matching the merged repository structure
from decisionlab.extract import extract_decisions
from decisionlab.verify import verify_decisions

def main():
    parser = argparse.ArgumentParser(
        description="IssueFlowP6: Open Source Decision Intelligence & Fact-Checking CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'extract' command
    parser_extract = subparsers.add_parser(
        "extract", help="Extract and verify decisions from a discussion text file."
    )
    parser_extract.add_argument(
        "input_file", type=str, help="Path to raw discussion file (e.g., examples/input/api_discussion.txt)"
    )
    parser_extract.add_argument(
        "--output", type=str, default="examples/output/recovered_decisions.json", help="Path to save verified JSON output"
    )

    # 'lookup' command
    parser_lookup = subparsers.add_parser(
        "lookup", help="Search through a saved verified JSON decisions file."
    )
    parser_lookup.add_argument(
        "decisions_file", type=str, help="Path to verified JSON file"
    )
    parser_lookup.add_argument(
        "--query", type=str, default="", help="Keyword to search in decisions or reasoning"
    )

    args = parser.parse_args()

    if args.command == "extract":
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' not found.")
            return

        discussion_text = input_path.read_text(encoding="utf-8")

        print(f"-> Reading & extracting decisions from {input_path} using qwen2.5:7b...")
        # Pass the actual file contents (not the path) to the model
        raw_result = extract_decisions(discussion_text)

        print(f"-> Running Srivastava's Fact-Checker verification engine...")
        # Fixed: Passes the list directly instead of trying to use .get()
        verified_result = verify_decisions(raw_result, discussion_text)

        # Save output
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(verified_result, indent=2), encoding="utf-8")

        stats = verified_result["verification_stats"]
        print("\n=== Factory Line Execution Complete ===")
        print(f"Total Extracted: {stats['total_extracted']}")
        print(f"Verified & Kept: {stats['verified_kept']}")
        print(f"Hallucinations Removed: {stats['hallucinations_removed']}")
        print(f"Saved verified output to: {out_path}")

    elif args.command == "lookup":
        dec_path = Path(args.decisions_file)
        if not dec_path.exists():
            print(f"Error: Decisions file '{dec_path}' not found.")
            return

        data = json.loads(dec_path.read_text(encoding="utf-8"))
        decisions = data.get("decisions", [])

        query = args.query.lower()
        print(f"\n=== Decision Lookup (Total: {len(decisions)}) ===")
        
        for idx, item in enumerate(decisions, start=1):
            # Fixed: Keys strictly match your extract.py data contract
            decision_text = item.get("decision", "")
            reason = item.get("reason", "")
            
            if query and query not in decision_text.lower() and query not in reason.lower():
                continue
                
            print(f"\n[{idx}] Status: {item.get('status', '').upper()}")
            print(f"    Decision: {decision_text}")
            print(f"    Reasoning: {reason}")
            print(f"    Alternative: {item.get('alternative', '')}")
            print(f"    Verified Quote: \"{item.get('quote', '')}\"")

if __name__ == "__main__":
    main()