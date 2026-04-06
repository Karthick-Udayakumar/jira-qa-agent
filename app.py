import streamlit as st
from tools.jira_tool import fetch_jira_story
from tools.testgen_tool import generate_test_cases

st.set_page_config(
    page_title="QA Test Case Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #21262d !important;
    padding-top: 1rem !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #c9d1d9 !important;
}
.block-container {
    padding: 1.5rem 2.5rem 3rem 2.5rem !important;
    max-width: 1200px !important;
}
[data-testid="stTextInput"] input {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1rem !important;
    font-family: 'SF Mono', monospace !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.12) !important;
    outline: none !important;
}
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    height: 42px !important;
}
[data-testid="stDownloadButton"] button {
    background: #161b22 !important;
    border: 1px solid #58a6ff !important;
    border-radius: 8px !important;
    color: #58a6ff !important;
    font-weight: 600 !important;
    width: 100% !important;
    padding: 0.6rem !important;
}
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
}
[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="metric-container"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.5rem !important;
}
table { width: 100% !important; border-collapse: collapse !important; font-size: 0.875rem !important; }
thead { background: #161b22 !important; }
th { padding: 12px 16px !important; color: #58a6ff !important; border-bottom: 2px solid #30363d !important; font-weight: 600 !important; text-align: left !important; text-transform: uppercase !important; letter-spacing: 0.4px !important; }
td { padding: 12px 16px !important; border-bottom: 1px solid #21262d !important; color: #c9d1d9 !important; vertical-align: top !important; line-height: 1.5 !important; }
tr:hover td { background: #161b22 !important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background-color: #161b22 !important;
    border-color: #30363d !important;
    color: #e6edf3 !important;
    border-radius: 8px !important;
}
hr { border-color: #21262d !important; margin: 1rem 0 !important; }
#MainMenu, footer, header { visibility: hidden !important; }
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "total_tc" not in st.session_state:
    st.session_state.total_tc = 0

# ── Sidebar ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧪 QA Agent")
    st.caption("Jira + Groq · llama-3.3-70b")
    st.divider()

    st.markdown("**Output Format**")
    output_format = st.selectbox(
        "fmt", ["Step-by-Step", "BDD (Given/When/Then)", "Table Format"],
        label_visibility="collapsed"
    )

    st.markdown("**Test Types**")
    test_types = st.multiselect(
        "types",
        ["Positive", "Negative", "BVA", "Edge Cases"],
        default=["Positive", "Negative", "BVA", "Edge Cases"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**🕘 Recent Issues**")
    if st.session_state.history:
        for k in reversed(st.session_state.history[-6:]):
            st.code(k, language=None)
    else:
        st.caption("None yet.")

    st.divider()
    st.markdown("""
    <div style="font-size:0.75rem; color:#484f58; line-height:2;">
    🔵 Jira REST API v3<br>
    ⚡ Groq · llama-3.3-70b<br>
    🐍 Python 3.14 · Streamlit
    </div>
    """, unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────
st.markdown("## 🧪 QA Test Case Generator")
st.markdown("Connect to **Jira** · Fetch user stories · Generate AI-powered test cases instantly.")
st.divider()

# ── Dashboard ──────────────────────────────────────────────────────
st.markdown("#### 📊 Dashboard")
d1, d2, d3, d4 = st.columns(4)
d1.metric("Stories Fetched",      len(st.session_state.history))
d2.metric("Test Cases Generated", st.session_state.total_tc)
d3.metric("Active Test Types",    len(test_types))
d4.metric("LLM Model",            "Llama 3.3-70b")

st.divider()

# ── Input ──────────────────────────────────────────────────────────
st.markdown("#### 🔍 Fetch Story & Generate")
col_in, col_btn = st.columns([5, 1])
with col_in:
    issue_key = st.text_input(
        "Jira Issue Key",
        placeholder="e.g.  SCRUM-2",
        label_visibility="collapsed"
    )
with col_btn:
    generate = st.button("⚡ Generate", type="primary", use_container_width=True)

# ── Agent ──────────────────────────────────────────────────────────
if generate:
    if not issue_key.strip():
        st.warning("Please enter a valid Jira issue key.")
        st.stop()

    key = issue_key.strip().upper()

    with st.spinner(f"📥 Fetching {key} from Jira..."):
        story = fetch_jira_story(key)

    if not story:
        st.error("Could not fetch story. Check your issue key and `.env` credentials.")
        st.stop()

    if key not in st.session_state.history:
        st.session_state.history.append(key)

    st.divider()
    st.markdown("##### 📋 Story Details")
    r1, r2, r3, r4 = st.columns([4, 1, 1, 1])
    r1.markdown(f"**{story['summary']}**")
    r2.info(story["key"])
    r3.info(story["type"])
    r4.info(story["status"])

    with st.expander("View Full Description & Acceptance Criteria"):
        st.markdown(story["description"] or "_No description provided._")

    st.divider()

    with st.spinner(f"🧠 Generating {output_format} test cases with Groq AI..."):
        test_cases = generate_test_cases(
            story,
            output_format=output_format,
            test_types=test_types
        )

    tc_count = test_cases.count("TC-") + test_cases.count("Scenario:")
    st.session_state.total_tc += max(tc_count, 1)

    st.markdown(f"##### ✅ Generated Test Cases — `{output_format}`")

    if output_format == "Table Format":
        st.markdown(test_cases)
    elif output_format == "BDD (Given/When/Then)":
        for scenario in test_cases.strip().split("\n\n"):
            if scenario.strip():
                st.markdown(scenario)
                st.markdown("---")
    else:
        for block in test_cases.strip().split("\n\n"):
            if block.strip():
                st.markdown(block)
                st.markdown("---")

    st.divider()
    output_text = "Test Cases: " + key + "\nFormat: " + output_format + "\n" + "="*60 + "\n\n" + test_cases
    st.download_button(
        label="⬇️ Download Test Cases (.txt)",
        data=output_text,
        file_name=key + "_test_cases.txt",
        mime="text/plain"
    )

    st.divider()
    st.markdown("#### 📊 Updated Dashboard")
    u1, u2, u3, u4 = st.columns(4)
    u1.metric("Stories Fetched",      len(st.session_state.history))
    u2.metric("Test Cases Generated", st.session_state.total_tc)
    u3.metric("Last Format",          output_format.split(" ")[0])
    u4.metric("Last Issue",           key)