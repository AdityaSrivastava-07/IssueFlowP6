# IssueFlow (decisionlab) — Decision Intelligence & Knowledge Recovery

> **Hacktoberfest 2026 — Team RAGA**  
> Problem Statement 6: Open Source Decision Intelligence and Knowledge Recovery

---

## 📌 Problem Overview

Open-source projects make critical architectural and technical decisions inside lengthy discussion threads (issues, pull requests, mailing lists, and PEPs). Over time:
- The reasoning behind choices is forgotten.
- Rejected alternatives are suggested repeatedly.
- New contributors make changes without knowing historical constraints.

**IssueFlow** extracts technical decisions, their accepted/rejected status, rejected alternatives, and rationales from engineering discussions. Crucially, it validates every extracted claim against an exact verbatim quote from the original source—discarding any hallucinated decisions.

---

## 🏗️ Architecture & Pipeline

```text
  Discussion Thread (.txt)
            │
            ▼
┌─────────────────────────┐
│   decisionlab/extract   │  Extracts decisions using local Qwen 2.5:7b via Ollama
└───────────┬─────────────┘
            │  Structured JSON (Decision, Status, Reason, Verbatim Quote)
            ▼
┌─────────────────────────┐
│   decisionlab/verify    │  Strict Anti-Hallucination Engine:
└───────────┬─────────────┘  Matches normalized quote against source; drops unverified items
            │
            ▼
┌─────────────────────────┐
│  examples/output/*.json │  Verified decision store with extraction & fact-check stats
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    decisionlab/cli      │  Lookup decisions by keyword, file, or topic
└─────────────────────────┘
```

---

## 🤖 AI Model & Runtime

- **Model:** `qwen2.5:7b` (or `qwen2.5:3b` for constrained environments)
- **Runtime:** [Ollama](https://ollama.com/) (100% local, zero cloud dependencies, no API keys needed)
- **Endpoint:** `http://localhost:11434/api/generate`

### Why Local Qwen 2.5?
- Reliable structured JSON output.
- Complete privacy and offline capability.
- Verifiable and cost-free local execution.

---

## 🛡️ Anti-Hallucination Guarantee (`verify.py`)

Judges and users do not need to trust the LLM blindly:
1. Every candidate decision extracted by the model **must** include an exact quote.
2. The verification engine normalizes whitespace and punctuation, then verifies that the quote exists verbatim in the source text.
3. Quotes shorter than 10 characters or invented quotes are **rejected and removed** from the output.
4. Output files include a `verification_stats` summary showing:
   - `total_extracted`
   - `verified_kept`
   - `hallucinations_removed`

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.11+**
2. **Ollama**:
   ```bash
   # Start Ollama
   ollama serve

   # Pull the model
   ollama pull qwen2.5:7b
   ```

### Installation

```bash
git clone https://github.com/AdityaSrivastava-07/IssueFlowP6.git
cd IssueFlowP6
pip install -r requirements.txt
```

---

## 💻 CLI Usage

### 1. Extract & Verify Decisions
Run the full extraction and fact-checking pipeline on a discussion:
```bash
python3 -m decisionlab.cli extract examples/input/parser_discussion.txt --output examples/output/parser_decisions.json
```

### 2. Lookup Past Decisions
Query saved decisions by keyword:
```bash
python3 -m decisionlab.cli lookup examples/output/parser_decisions.json --query "yaml"
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

The test suite validates:
- Quote normalization and verification.
- Elimination of hallucinated decisions and fake quotes.

---

## 📁 Repository Structure

```text
IssueFlowP6/
├── .github/
│   ├── pull_request_template.md    # Standard PR template
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI workflow (pytest)
├── decisionlab/
│   ├── __init__.py
│   ├── extract.py                  # Local Ollama / Qwen extraction
│   ├── verify.py                   # Strict quote verification engine
│   └── cli.py                      # Command-line interface (extract & lookup)
├── docs/
│   └── demo-script.md              # 2-minute live demo guide
├── examples/
│   ├── input/                      # Sample synthetic discussions (API, DB, Parser)
│   └── output/                     # Verified output decision files
├── tests/
│   └── test_verify.py              # Anti-hallucination verification tests
├── aliases.json                    # Contributor identity normalization
├── HACKATHON.md                    # Hackathon team details and scope
├── LICENSE                         # MIT License
├── README.md                       # Documentation
└── requirements.txt                # Dependencies (requests, pytest)
```

---

## ⚠️ Known Limitations & Honesty

- **Local Latency:** Running a 7B parameter model locally on CPU/Metal takes ~15–30 seconds per thread.
- **Quote Exactness:** If the LLM subtly paraphrases a valid point rather than quoting verbatim, the strict verifier will discard it to prevent false history.
- **Single Thread Scope:** Currently processes discussion threads one at a time. Multi-thread cross-referencing is a target for future iterations.

---

## 👥 Team RAGA (Hack Day Sonipat 2026)

- **Resmanth Kumar Beesetti** — Specification, Documentation & Demo
- **Gagandeep** — Core Builder & Pipeline
- **Aditya Srivastava** — Testing, Sample Data & Verification
- **Aditya Dhanraj Singh** — Repository, PRs & CI Automation
