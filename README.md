<div align="center">

# ⛏️ D-MINE
**Decision-Mining & Intelligence Recovery Engine**

[![Hacktoberfest](https://img.shields.io/badge/Hack_Day-Sonipat-FA7B59?style=for-the-badge&logo=hackaday&logoColor=white)](#)
[![Track 6](https://img.shields.io/badge/Track-Problem_6-2EA043?style=for-the-badge)](#)
[![Model](https://img.shields.io/badge/AI_Engine-Qwen_2.5:7b-3B82F6?style=for-the-badge&logo=ollama)](#)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local-A371F7?style=for-the-badge)](#)

*Your pull request just broke production. Do you know why this architecture was chosen 3 years ago?*<br>
*Neither does anyone else.*

</div>

## ⚠️ The Problem
Enterprise knowledge dies in closed pull requests and lost Slack threads. When code breaks, developers waste hours reverse-engineering technical decisions because the original reasoning was never documented. 

## 💡 The D-MINE Solution
D-MINE is a privacy-first, local AI pipeline that scrapes raw developer discussions, uses an LLM to extract the hidden architectural decisions, and ruthlessly purges hallucinations before saving the truth to an instantly searchable database. 

## 🏗️ System Architecture

```text
[ GitHub / Forums ] 
       │
       ▼ (gh cli)
[ Raw Discussion Text ] ──▶ 🧠 Qwen 2.5 (Local LLM)
                                 │ Extracts Decisions
                                 ▼
                         🛡️ Fact-Checker
                         (Strict 100% Quote Verification)
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
   ❌ Hallucinations                             ✅ Verified JSON
   (Dropped & Purged)                          (Saved to Database)
                                                       │
                                                       ▼
                                              🔎 D-MINE Lookup CLI

```

---

## 🔥 Key Features

* **100% Local & Private:** Runs entirely on your machine via Ollama. No proprietary enterprise code is ever sent to OpenAI or third-party APIs.
* **Aggressive Anti-Hallucination:** Our custom `verify.py` engine guarantees that every extracted decision is backed by a verbatim quote from the source text. If the AI hallucinates, the data is dropped.
* **Instant Knowledge Retrieval:** A blazing-fast CLI search tool to query historical technical decisions in seconds.

---

## ⚙️ Quick Start & Installation

D-MINE requires Python 3.x and [Ollama](https://ollama.com/) to run the local AI model.

### 1. Initialize the Environment

```bash
# Clone the repository
git clone [https://github.com/AdityaSrivastava-07/IssueFlowP6.git](https://github.com/AdityaSrivastava-07/IssueFlowP6.git)
cd IssueFlowP6
pip install -r requirements.txt

# Start Ollama and pull the extraction model
ollama pull qwen2.5:7b

```

### 2. The Scrape Phase

Use the GitHub CLI to download a raw PR thread, stripping away UI noise for a clean context window:

```bash
gh pr view 14853 --repo facebook/react --comments > examples/input/demo_pr.txt

```

### 3. The Extraction Phase

Feed the raw text into the D-MINE pipeline. Watch the Fact-Checker validate quotes in real-time:

```bash
python3 -m decisionlab.cli extract examples/input/demo_pr.txt --output decisions.json

```

### 4. The Retrieval Phase

Query your new knowledge base to instantly recover lost context:

```bash
python3 -m decisionlab.cli lookup decisions.json --query "concurrent mode"

```

---

## 👥 The Team RAGA

Built for Hack Day Sonipat — Problem Statement 6.

* **Aditya Dhanraj Singh**
* **Resmanth Kumar Beesetti**
* **Gagandeep**
* **Aditya Srivastava**

