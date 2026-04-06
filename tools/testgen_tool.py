import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

FORMAT_PROMPTS = {
    "BDD (Given/When/Then)": """Format EVERY test case in Gherkin BDD:

**Scenario: <Title>**
- **Type:** <Positive | Negative | BVA | Edge Case>
- **Given** <precondition>
- **When** <action>
- **Then** <expected result>

Separate each scenario with a blank line.""",

    "Step-by-Step": """Format EVERY test case exactly like this:

**TC-XX | <TYPE> | <Title>**
**Steps:**
1. <Step 1>
2. <Step 2>
3. <Step 3>
**Expected Result:** <what should happen>

Separate each test case with a blank line.""",

    "Table Format": """Output ALL test cases as one markdown table:

| TC ID | Type | Title | Steps | Expected Result |
|-------|------|-------|-------|-----------------|

Steps column: use semicolons between steps. Keep cells concise. No text outside the table."""
}


def generate_test_cases(
    story: dict,
    output_format: str = "Step-by-Step",
    test_types: list = None
) -> str:

    if not test_types:
        test_types = ["Positive", "Negative", "BVA", "Edge Cases"]

    # Build explicit instruction for each type
    type_instructions = {
        "Positive":    "✅ POSITIVE: Happy path, valid inputs, successful outcomes (minimum 3 test cases)",
        "Negative":    "❌ NEGATIVE: Invalid inputs, error messages, failure scenarios (minimum 3 test cases)",
        "BVA":         "🔲 BVA: Exact minimum, maximum, just below min, just above max values (minimum 3 test cases)",
        "Edge Cases":  "⚠️  EDGE: Empty values, concurrent actions, timeouts, special characters (minimum 2 test cases)"
    }

    selected_instructions = "\n".join(
        type_instructions[t] for t in test_types if t in type_instructions
    )

    format_instruction = FORMAT_PROMPTS.get(output_format, FORMAT_PROMPTS["Step-by-Step"])

    system_prompt = f"""You are a senior QA engineer with 10+ years of experience.

YOU MUST generate test cases for ALL of the following types. Do NOT skip any type:

{selected_instructions}

{format_instruction}

IMPORTANT:
- Generate test cases for EVERY type listed above
- Label each test case clearly with its type
- Be specific with values, limits, and error messages from the acceptance criteria
- Do not stop after positive test cases"""

    user_message = f"""
Issue Key   : {story.get('key', 'N/A')}
Type        : {story.get('type', 'Story')}
Priority    : {story.get('priority', 'Medium')}
Summary     : {story.get('summary', '')}
Description : {story.get('description', 'No description provided.')}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.2,
        max_tokens=4000
    )

    return response.choices[0].message.content