# Hacktoberfest 2026 --- HACKATHON.md

## Team Information

-   **Team Name:** RAGA
-   **Event:** Hacktoberfest 2026
-   **Institution:** Newton School of Technology, Rishihood University

## Team Members

  ----------------------------------------------------------------------------------------------------------------
  Name                    GitHub Username                                                  Role
  ----------------------- ---------------------------------------------------------------- -----------------------
  Aditya Srivastava       [@AdityaSrivastava-07](https://github.com/AdityaSrivastava-07)   Not specified

  Gagandeep               [@gagandeep3016-sudo](https://github.com/gagandeep3016-sudo)     Not specified

  Resmanth Kumar Beesetti [@resmanth](https://github.com/resmanth)                         Not specified

  Aditya Dhanraj Singh    [@adityasingh916](https://github.com/adityasingh916)             Not specified
  ----------------------------------------------------------------------------------------------------------------

## Selected Problem Statement

**Problem Statement 6: Open Source Decision Intelligence and Knowledge
Recovery**

**Focus:** Knowledge Management & Information Retrieval

### Problem Overview

Open-source projects accumulate important technical knowledge across
discussions, issues, and pull requests. Architectural decisions, the
reasoning behind them, and alternatives that were rejected can become
difficult to find when contributors revisit related parts of a codebase.

The goal of this project is to recover and organize that knowledge so it
can be surfaced when new code changes touch relevant areas.

## Project Overview

RAGA is building an open-source decision-intelligence and
knowledge-recovery platform. The platform will analyze historical
project discussions, issues, and pull-request threads to identify
architectural decisions, their rationale, rejected alternatives, and
supporting quotes. It will organize the extracted information and make
relevant decisions easier to retrieve when new code changes affect
related areas.

## AI Model

-   **Model:** Qwen 2.5
-   **Runtime:** Ollama (local execution)

### Model Justification

Qwen 2.5 will run locally through Ollama, without depending on a cloud
service or requiring API keys. It is selected because it can produce
structured JSON reliably, which the project pipeline needs to store
extracted decisions, rejected alternatives, and supporting quotes in a
consistent format.

## Project Scope

The planned workflow is to:

1.  Parse historical project discussions, issues, and pull-request
    threads.
2.  Extract architectural decisions and the rationale behind them.
3.  Capture rejected alternatives and supporting quotes.
4.  Store the extracted knowledge in a structured, retrievable format.
5.  Surface relevant historical decisions when new code changes touch
    related areas.

## Repository

-   **Repository Name:** `IssueFlowP6`
-   **Repository URL:** To be added after repository creation.

------------------------------------------------------------------------

*This document records the team's selected problem statement, project
direction, team details, and intended AI model usage for Hacktoberfest
2026.*
