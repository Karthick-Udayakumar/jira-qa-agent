import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()


def fetch_jira_story(issue_key: str) -> dict:
    url = f"{os.getenv('JIRA_URL')}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, auth=auth, timeout=10)
    except Exception as e:
        print(f"Connection error: {e}")
        return {}

    if response.status_code != 200:
        print(f"Jira Error {response.status_code}: {response.text}")
        return {}

    data   = response.json()
    fields = data.get("fields", {})

    summary    = fields.get("summary", "No summary")
    description = fields.get("description", {})
    issue_type = fields.get("issuetype", {}).get("name", "Story")
    status     = fields.get("status",    {}).get("name", "Unknown")
    priority   = fields.get("priority",  {}).get("name", "Medium")

    desc_text = extract_adf_text(description) if isinstance(description, dict) else str(description or "")

    print(f"Fetched: [{issue_key}] {summary}")

    return {
        "key":         issue_key,
        "type":        issue_type,
        "status":      status,
        "priority":    priority,
        "summary":     summary,
        "description": desc_text
    }


def extract_adf_text(node) -> str:
    if not node or not isinstance(node, dict):
        return ""
    if node.get("type") == "text":
        return node.get("text", "")
    parts = [extract_adf_text(child) for child in node.get("content", [])]
    return "\n".join(p for p in parts if p.strip())