# Demo Script (2 minutes)

## 0:00-0:15 — Introduction
- Welcome. DevMemory (IssueFlow) recovers architectural decisions from historical
  engineering discussions, issues, and pull requests.
- Note: all sample discussions are synthetic example data.

## 0:15-0:45 — Sample discussion data
- Open examples/input/ and show the three synthetic discussions:
  parser_discussion.txt, database_discussion.txt, api_discussion.txt.
- Point out each contains multiple contributors, conflicting opinions, proposed
  changes, rejected alternatives with reasons, and a clear final decision.

## 0:45-1:15 — Contributor identity mapping
- Open aliases.json. Show fictional usernames mapped to canonical contributor IDs.
- Explain that normalization lets us attribute decisions to one person across
  multiple usernames/aliases.

## 1:15-1:45 — Pipeline walkthrough
- Mention the parser and extraction/verification steps (cli.py, decisionlab/)
  consume these inputs to produce structured decisions. These components are
  owned by other contributors and are not modified here.

## 1:45-2:00 — Wrap-up
- Show examples/output/ as the destination for generated artifacts.
- Invite questions and feedback.
