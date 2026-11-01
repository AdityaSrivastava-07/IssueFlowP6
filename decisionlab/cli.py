"""
Command-Line Interface for IssueFlow (Team RAGA - Problem 6).
Provides subcommands:
  - extract: Ingests discussion thread, runs local Qwen 2.5 extraction and quote verification.
  - lookup: Queries recovered decisions by keyword/topic.
"""

import argparse
import json
import sys
from pathlib import Path

from decisionlab.extract import extract_decisions
from decisionlab.verify import verify_decisions


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="issueflow",
        description="IssueFlow: Open Source Decision Intelligence & Knowledge Recovery CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: extract
    parser_extract = subparsers.add_parser(
        "extract",
        help="Extract and verify technical decisions from a discussion thread file.",
    )
    parser_extract.add_argument(
        "input_file",
        type=str,
        help="Path to raw discussion file (e.g., examples/input/api_discussion.txt)",
    )
    parser_extract.add_argument(
        "--output",
        "-o",
        type=str,
        default="examples/output/recovered_decisions.json",
        help="Path to save verified JSON output (default: examples/output/recovered_decisions.json)",
    )

    # Command: lookup
    parser_lookup = subparsers.add_parser(
        "lookup",
        help="Search through a saved verified decisions file.",
    )
    parser_lookup.add_argument(
        "decisions_file",
        type=str,
        help="Path to verified JSON file (e.g., examples/output/parser_decisions.json)",
    )
    parser_lookup.add_argument(
        "--query",
        "-q",
        type=str,
        default="",
        help="Keyword to filter decisions, alternatives, or reasons",
    )

    return parser


def handle_extract(args: argparse.Namespace) -> int:
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return 1

    discussion_text = input_path.read_text(encoding="utf-8")

    print(f"-> Reading & extracting decisions from '{input_path}' using Qwen 2.5:7b...")
    try:
        raw_result = extract_decisions(discussion_text)
    except Exception as err:
        print(f"Extraction failed: {err}", file=sys.stderr)
        return 1

    print("-> Running strict anti-hallucination verification engine...")
    verified_result = verify_decisions(raw_result, discussion_text)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(verified_result, indent=2), encoding="utf-8")

    stats = verified_result["verification_stats"]
    print("\n=== Extraction & Verification Summary ===")
    print(f"Total Extracted         : {stats['total_extracted']}")
    print(f"Verified & Retained     : {stats['verified_kept']}")
    print(f"Hallucinations Rejected : {stats['hallucinations_removed']}")
    print(f"Output saved to         : {out_path}\n")
    return 0


def handle_lookup(args: argparse.Namespace) -> int:
    dec_path = Path(args.decisions_file)
    if not dec_path.exists():
        print(f"Error: Decisions file '{dec_path}' not found.", file=sys.stderr)
        return 1

    try:
        data = json.loads(dec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        print(f"Error: Failed to parse JSON file '{dec_path}': {err}", file=sys.stderr)
        return 1

    decisions = data.get("decisions", [])
    query = args.query.lower().strip()

    print(f"\n=== Decision Lookup (Total in file: {len(decisions)}) ===")
    matched_count = 0

    for idx, item in enumerate(decisions, start=1):
        decision_text = str(item.get("decision", ""))
        reason = str(item.get("reason", ""))
        alternative = str(item.get("alternative", ""))

        if query:
            haystack = f"{decision_text} {reason} {alternative}".lower()
            if query not in haystack:
                continue

        matched_count += 1
        status = str(item.get("status", "UNSPECIFIED")).upper()
        print(f"\n[{matched_count}] Status: {status}")
        print(f"    Decision  : {decision_text}")
        if reason:
            print(f"    Reasoning : {reason}")
        if alternative:
            print(f"    Alternative Rejected: {alternative}")
        print(f"    Verified Quote: \"{item.get('quote', '')}\"")

    if matched_count == 0:
        print(f"\nNo decisions matched query: '{query}'")
    else:
        print(f"\nTotal matches: {matched_count}\n")

    return 0


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "extract":
        sys.exit(handle_extract(args))
    elif args.command == "lookup":
        sys.exit(handle_lookup(args))


if __name__ == "__main__":
    main()
