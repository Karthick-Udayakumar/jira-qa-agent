from tools.jira_tool import fetch_jira_story
from tools.testgen_tool import generate_test_cases

def run():
    print("\n🤖 QA Test Case Generator Agent")
    print("=" * 50)

    issue_key = input("Enter Jira Issue Key (e.g. SCRUM-2): ").strip().upper()

    # Step 1: Fetch from Jira
    print(f"\n📥 Fetching story from Jira...")
    story = fetch_jira_story(issue_key)

    if not story:
        print("❌ Could not fetch story. Check your issue key and .env credentials.")
        return

    print(f"\n📋 Story Details:")
    print(f"   Key      : {story['key']}")
    print(f"   Summary  : {story['summary']}")
    print(f"   Priority : {story['priority']}")
    print(f"   Status   : {story['status']}")

    # Step 2: Generate test cases via Groq
    print(f"\n⚙️  Generating test cases via Groq...")
    test_cases = generate_test_cases(story)

    print("\n" + "=" * 50)
    print("✅ GENERATED TEST CASES")
    print("=" * 50)
    print(test_cases)

    # Step 3: Save to file
    output_file = f"{issue_key}_test_cases.txt"
    with open(output_file, "w") as f:
        f.write(f"Test Cases for {issue_key}: {story['summary']}\n")
        f.write("=" * 50 + "\n\n")
        f.write(test_cases)

    print(f"\n💾 Saved to: {output_file}")

if __name__ == "__main__":
    run()