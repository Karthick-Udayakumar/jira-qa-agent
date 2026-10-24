# QA Test Case Generator (Jira + Groq)

An AI-powered QA agent that reads a **Jira user story**, asks an LLM to act as a senior QA engineer, and returns **Positive, Negative, Boundary Value Analysis (BVA), and Edge-case test cases**. You can use it from a Streamlit web UI or from a command-line agent that saves the results to a text file.

It turns a story's acceptance criteria into structured, reviewable test cases in a few seconds, which saves the first-draft effort that usually goes into test design.

## Features

- **Jira integration.** Fetches a story by issue key through the Jira Cloud REST API v3 (summary, type, priority, status, description). Descriptions in Atlassian Document Format are converted to plain text.
- **Four test types:**

  | Type | What the LLM is asked to produce |
  |---|---|
  | Positive | Happy-path scenarios with valid inputs (at least 3) |
  | Negative | Invalid inputs, error messages, and failure scenarios (at least 3) |
  | BVA | Exact minimum and maximum, values just below the minimum, and just above the maximum (at least 3) |
  | Edge Cases | Empty values, concurrent actions, timeouts, and special characters (at least 2) |

- **Three output formats:** Step-by-Step, Table (markdown table), and BDD (Given / When / Then).
- **Streamlit UI** with a format selector, test-type multi-select, metrics, and a download button for the generated file.
- **CLI agent** (`agent.py`) that prompts for an issue key and writes `<ISSUE-KEY>_test_cases.txt`.
- **Model:** `llama-3.3-70b-versatile` on Groq.

## Architecture

```
Jira issue key → tools/jira_tool.py      (fetch story via Jira REST API v3)
              → tools/testgen_tool.py    (build prompt → Groq chat completion)
              → app.py (Streamlit UI)  or  agent.py (CLI → .txt file)
```

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI: issue key input, format and test-type selection, results, download |
| `agent.py` | Command-line flow: fetch → generate → save |
| `tools/jira_tool.py` | Jira REST API client and Atlassian Document Format text extraction |
| `tools/testgen_tool.py` | Prompt construction per test type and output format, Groq call |
| `.env.example` | Template for the four required environment variables |

## Prerequisites

- Python 3
- A Jira Cloud site and an API token for your account (create one at Atlassian account settings → Security → API tokens)
- A Groq API key

## Setup

```bash
git clone https://github.com/Karthick-Udayakumar/jira-qa-agent.git
cd jira-qa-agent

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Edit `.env`:

```bash
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your@email.com
JIRA_API_TOKEN=your_jira_api_token
GROQ_API_KEY=your_groq_api_key
```

Keep `.env` out of version control. It is already covered by `.gitignore`.

## Usage

### Web UI

```bash
streamlit run app.py
```

Enter a Jira key such as `SCRUM-2`, choose an output format and test types, then click **Generate**.

### Command line

```bash
python3 agent.py
```

Enter an issue key when prompted. The result prints to the terminal and is saved as `<ISSUE-KEY>_test_cases.txt` in the current folder.

## Example

The repository includes `SCRUM-2_test_cases.txt`, which shows real output for a sample story about transferring money through a UPI ID. Each case has an ID, a type, a title, numbered steps, and an expected result.

## Limitations

- Output quality depends on the story. Vague acceptance criteria produce vague test cases.
- The LLM can invent limits, messages, or flows that the story does not specify. Review every generated case before use.
- The Jira client reads only the fields listed above. Attachments, comments, and linked issues are not used.

## Roadmap

- Add a reviewer step that flags test cases that do not trace to an acceptance criterion.
- Export directly to Xray, Zephyr, or Azure Test Plans.
- Add a prompt-evaluation set to measure how changes affect output quality.

## Author

**Karthick Udayakumar**: AI/QA engineering leader focused on AI-first test automation.
[LinkedIn](https://www.linkedin.com/in/karthick-udayakumar) · karthick2490@gmail.com
