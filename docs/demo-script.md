# Demo Script (2 minutes)

## 0:00-0:15 — Introduction
- Welcome. DevMemory (IssueFlow) aims to recover architectural decisions from
  historical engineering discussions, issues, and pull requests.
- Note: all sample discussions used in this demo are synthetic example data.

## 0:15-0:45 — Sample discussion data
- Open examples/input/ and show the three synthetic discussions:
  parser_discussion.txt, database_discussion.txt, api_discussion.txt.
- Point out each contains multiple contributors, conflicting opinions, proposed
  changes, rejected alternatives with reasons, and a clear final decision.

## 0:45-1:15 — Contributor identity mapping
- Open aliases.json. Show fictional usernames mapped to canonical contributor IDs.
- Explain that normalization lets us attribute decisions to one person across
  multiple usernames/aliases.

## 1:15-1:45 — Pipeline and outputs
- Explain that these inputs feed the team's extraction/verification pipeline
  (owned by teammates), which produces structured decision records.
- Show examples/output/ as the destination for generated artifacts.

## 1:45-2:00 — Wrap-up
- Summarize: synthetic test data plus identity mapping support reproducible
  evaluation of decision extraction.
- Invite questions and feedback.
