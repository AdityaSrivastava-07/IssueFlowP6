<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=250&section=header&text=D-Mine&fontSize=90&animation=fadeIn" width="100%" />

  **Decision Intelligence & Knowledge Recovery Engine**
  
  [![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-Hack_Day_Sonipat-FA7B59?style=for-the-badge&logo=hackaday&logoColor=white)](#)
  [![Problem 6](https://img.shields.io/badge/Track-Problem_6-2EA043?style=for-the-badge)](#)
  [![Qwen 2.5](https://img.shields.io/badge/Model-Qwen_2.5:7b_Local-3B82F6?style=for-the-badge&logo=ollama)](#)
  [![License: MIT](https://img.shields.io/badge/License-MIT-A371F7?style=for-the-badge)](#)
</div>

<br>

## 🌪️ The Vision
When a pull request breaks production, developers waste hours digging through old Slack threads, reverted PRs, and messy issues to figure out *why* a specific architecture was chosen. **IssueFlow** recovers the decisions nobody wrote down. We extract lost context, run it through an anti-hallucination verification engine, and surface it instantly.

---

## 🚀 Hackathon Submission Info
<details>
<summary><b>Click to expand Team & Track details</b></summary>

- **Track:** Problem 6 (Recover the decisions nobody wrote down)
- **AI Models Used:** `qwen2.5:7b` (Run locally via Ollama to ensure offline capability and privacy). AI coding assistants were used for GitHub Actions CI boilerplate and regex debugging.
- **Team Name:** [Insert Team Name]
- **Members:** [Insert Member 1], [Insert Member 2], [Insert Member 3], [Insert Member 4]
</details>

---

## ⚡ Core Architecture

| Module | Description | Tech Stack |
| :--- | :--- | :--- |
| **`extract`** | Parses raw developer discussions (issues, forum threads) and extracts structural decisions. | Python, Ollama (Qwen 2.5) |
| **`verify`** | A strict fact-checking engine that catches and drops LLM hallucinations before they are saved. | Pytest, Custom Logic |
| **`lookup`** | Terminal-based search engine to instantly query the verified JSON output for historical context. | Python `argparse` |

---

## 💻 Quick Start Guide

**1. Run the Extraction Engine**
Feed a raw discussion file into the pipeline. The AI will extract decisions and the fact-checker will purge any hallucinations.
```bash
python3 -m decisionlab.cli extract examples/input/database_discussion.txt --output examples/output/recovered.json