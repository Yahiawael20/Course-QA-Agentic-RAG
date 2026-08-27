import os
import re
import sys
import traceback

import streamlit as st

# ======================================================================
# PAGE CONFIG
# ======================================================================

st.set_page_config(
    page_title="Course QA Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# CUSTOM CSS
# ======================================================================

CUSTOM_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-0: #0a0e17;
    --bg-1: #0f1420;
    --card-bg: rgba(255, 255, 255, 0.045);
    --card-border: rgba(255, 255, 255, 0.09);
    --accent-1: #7c5cff;
    --accent-2: #22d3ee;
    --accent-3: #f472b6;
    --text-main: #e8ebf5;
    --text-dim: #9aa3b8;
    --success: #34d399;
    --warning: #fbbf24;
    --danger: #f87171;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-main);
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(124, 92, 255, 0.16), transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(34, 211, 238, 0.12), transparent 45%),
        radial-gradient(circle at 50% 100%, rgba(244, 114, 182, 0.08), transparent 55%),
        linear-gradient(180deg, var(--bg-0) 0%, var(--bg-1) 100%);
    background-attachment: fixed;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1100px;}

/* ---------------- Header ---------------- */
.app-header {text-align: center; margin-bottom: 0.5rem;}
.app-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
}
.app-subtitle {
    color: var(--text-dim);
    font-size: 1.02rem;
    font-weight: 400;
    margin-bottom: 1.2rem;
}

/* ---------------- Badges ---------------- */
.badge-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    margin-bottom: 2rem;
}
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--card-border);
    color: var(--text-main);
    backdrop-filter: blur(10px);
}

/* ---------------- Glass Card ---------------- */
.glass-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    animation: fadeIn 0.45s ease;
}
.card-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}

/* ---------------- Section label ---------------- */
.section-label {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-dim);
    margin-bottom: 0.5rem;
    letter-spacing: 0.01em;
}

/* ---------------- Inputs ---------------- */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 14px !important;
    color: var(--text-main) !important;
    font-size: 1rem !important;
    padding: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent-1) !important;
    box-shadow: 0 0 0 3px rgba(124, 92, 255, 0.2) !important;
}

/* ---------------- Buttons ---------------- */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: 1px solid var(--card-border) !important;
    transition: all 0.2s ease !important;
    padding: 0.55rem 1.1rem !important;
}
div[data-testid="column"]:nth-of-type(1) .stButton > button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, var(--accent-1), #9c7bff) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(124, 92, 255, 0.35);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(124, 92, 255, 0.5);
}
.stButton > button:not([kind="primary"]) {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-main) !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: rgba(255, 255, 255, 0.09) !important;
    border-color: var(--accent-2) !important;
}

/* Example question chips */
.example-btn .stButton > button {
    width: 100%;
    text-align: left;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 0.9rem !important;
    background: rgba(255, 255, 255, 0.035) !important;
    color: var(--text-dim) !important;
}
.example-btn .stButton > button:hover {
    color: var(--text-main) !important;
    border-color: var(--accent-1) !important;
}

/* ---------------- Source cards ---------------- */
.source-card {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}
.source-card .src-icon {font-size: 1.2rem;}
.source-card .src-page {
    margin-left: auto;
    color: var(--text-dim);
    font-size: 0.8rem;
    background: rgba(255, 255, 255, 0.05);
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
}

/* ---------------- Workflow ---------------- */
.workflow-wrap {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    padding: 0.5rem 0;
}
.workflow-step {
    padding: 0.55rem 1rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
    white-space: nowrap;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    box-shadow: 0 4px 14px rgba(124, 92, 255, 0.25);
}
.workflow-step.final {
    background: linear-gradient(135deg, var(--success), var(--accent-2));
}
.workflow-arrow {
    color: var(--text-dim);
    font-size: 1.1rem;
    padding: 0 0.1rem;
}

/* ---------------- Planner card ---------------- */
.planner-row {display: flex; gap: 1.2rem; flex-wrap: wrap;}
.planner-item {flex: 1; min-width: 220px;}
.planner-value {
    display: inline-block;
    margin-top: 0.3rem;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
    background: linear-gradient(90deg, rgba(124,92,255,0.25), rgba(34,211,238,0.25));
    border: 1px solid var(--card-border);
}
.planner-reason {color: var(--text-dim); margin-top: 0.4rem; font-size: 0.92rem; line-height: 1.4;}

/* ---------------- Quiz cards ---------------- */
.quiz-card {
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
}
.quiz-q-num {
    display: inline-block;
    background: linear-gradient(90deg, var(--accent-1), var(--accent-3));
    color: white;
    font-weight: 700;
    font-size: 0.78rem;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    margin-bottom: 0.5rem;
}
.quiz-option {
    padding: 0.4rem 0.7rem;
    border-radius: 8px;
    margin: 0.25rem 0;
    font-size: 0.9rem;
    background: rgba(255, 255, 255, 0.03);
}
.quiz-answer {
    margin-top: 0.6rem;
    padding: 0.4rem 0.8rem;
    border-radius: 8px;
    background: rgba(52, 211, 153, 0.12);
    border: 1px solid rgba(52, 211, 153, 0.35);
    color: var(--success);
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

/* ---------------- DataFrame ---------------- */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid var(--card-border) !important;
}

/* ---------------- Comparison table (custom HTML) ---------------- */
.comparison-wrap {
    overflow-x: auto;
    border-radius: 14px;
    border: 1px solid var(--card-border);
}
.comparison-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    min-width: 640px;
}
.comparison-table thead th {
    background: linear-gradient(90deg, rgba(124, 92, 255, 0.28), rgba(34, 211, 238, 0.2));
    padding: 0.8rem 1.1rem;
    text-align: center;
    font-weight: 700;
    color: var(--text-main);
    white-space: nowrap;
    position: sticky;
    top: 0;
}
.comparison-table tbody td {
    padding: 0.75rem 1.1rem;
    text-align: center;
    vertical-align: top;
    line-height: 1.55;
    border-top: 1px solid var(--card-border);
    word-break: break-word;
}
.comparison-table tbody tr:nth-child(even) {
    background: rgba(255, 255, 255, 0.03);
}
.comparison-table tbody tr:hover {
    background: rgba(124, 92, 255, 0.08);
}
.comparison-table strong {
    color: var(--accent-2);
}

/* ---------------- Sidebar ---------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(15, 20, 32, 0.98), rgba(10, 14, 23, 0.98));
    border-right: 1px solid var(--card-border);
}
.sidebar-title {font-size: 1.3rem; font-weight: 800; margin-bottom: 0.2rem;}
.sidebar-sub {color: var(--text-dim); font-size: 0.85rem; margin-bottom: 1.4rem;}
.sidebar-section-title {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-dim);
    margin: 1.1rem 0 0.5rem 0;
    font-weight: 700;
}
.sidebar-chip {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    margin: 0.15rem 0.25rem 0.15rem 0;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--card-border);
    font-size: 0.8rem;
}
.sidebar-tool {font-size: 0.88rem; margin: 0.3rem 0; color: var(--text-main);}
.sidebar-stack {font-size: 0.85rem; color: var(--text-dim); line-height: 1.9;}

/* ---------------- Footer ---------------- */
.app-footer {
    text-align: center;
    color: var(--text-dim);
    font-size: 0.82rem;
    margin-top: 2.5rem;
    padding-top: 1.4rem;
    border-top: 1px solid var(--card-border);
}
.app-footer b {color: var(--text-main);}

/* ---------------- Alerts ---------------- */
.error-card {
    background: rgba(248, 113, 113, 0.08);
    border: 1px solid rgba(248, 113, 113, 0.35);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    color: #fca5a5;
    font-size: 0.9rem;
}

hr {border-color: var(--card-border) !important;}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ======================================================================
# BACKEND INTEGRATION
# ======================================================================

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

TOOL_DISPLAY_NAMES = {
    "retrieve": "Retrieval Tool",
    "summary": "Summary Tool",
    "compare": "Compare Tool",
    "quiz": "Quiz Tool",
}

PLANNER_REASONS = {
    "retrieve": "The question asks for a direct explanation, definition, or fact.",
    "summary": "The user requested a summary or overview of a topic.",
    "compare": "The user requested a comparison between two or more concepts.",
    "quiz": "The user requested quiz or practice questions.",
}

# Keyword safety net: the backend planner (LLM) sometimes misses one of the
# requested tools in compound questions (e.g. "compare X and Y and make a
# quiz about it" -> planner only returns a "compare" step). If the question
# clearly mentions a tool that the planner's steps don't already cover, we
# add that step ourselves so the requested tool still runs.
TOOL_KEYWORDS = {
    "compare": ["compare", "difference between", "differences between", " vs ", "versus"],
    "quiz": ["quiz", "mcq", "mcqs", "practice question", "practice questions", "test me", "make a test"],
    "summary": ["summarize", "summarise", "summary", "overview", "key points"],
}


def augment_plan_with_keywords(question: str, steps: list) -> list:
    """Append a step for any tool clearly requested in `question` but missing from `steps`."""
    existing_tools = {step["tool"] for step in steps}
    question_lower = question.lower()

    for tool_name, keywords in TOOL_KEYWORDS.items():
        if tool_name in existing_tools:
            continue
        if any(keyword in question_lower for keyword in keywords):
            steps.append({"tool": tool_name, "input": question})

    return steps


@st.cache_resource(show_spinner=False)
def load_agent():
    """Load the backend CourseAgent once and cache it across reruns."""
    from agent.agent import CourseAgent
    return CourseAgent()


def parse_tool_output(raw_output: str):
    """
    Split a tool's raw string output (answer + trailing 'Sources:' block)
    into clean answer text and a list of {"file", "page"} dicts.
    """
    if "Sources:" in raw_output:
        answer_part, sources_part = raw_output.rsplit("Sources:", 1)
    else:
        answer_part, sources_part = raw_output, ""

    answer_part = answer_part.strip()

    sources = []
    for line in sources_part.strip().splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        match = re.match(r"(.+?)\s*\(Page\s*(\d+)\)", line, re.IGNORECASE)
        if match:
            sources.append({"file": match.group(1).strip(), "page": int(match.group(2))})
        else:
            sources.append({"file": line, "page": None})

    return answer_part, sources


def extract_markdown_table(text: str):
    """Convert the first markdown table found in `text` into a list of row dicts."""
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return None

    header = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))

    return rows if rows else None


def md_bold_to_html(text: str) -> str:
    """Convert markdown **bold** into <strong> for safe inline HTML rendering."""
    if not text:
        return ""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def get_agent_response(question: str) -> dict:
    """
    Run `question` through the backend Agentic RAG pipeline and normalize
    the result into the single response shape the UI renders from:

        {
            "answer": str,
            "sources": [{"file", "page"}, ...],
            "planner": {"selected_tool", "reason"},
            "workflow": [str, ...],
            "comparison_table": [dict, ...] | None,
        }
    """
    agent = load_agent()

    plan = agent.planner.plan(question)
    steps = plan.get("steps", [])
    steps = augment_plan_with_keywords(question, steps)

    answer_chunks = []
    all_sources = []
    workflow = ["Question", "Planner"]
    comparison_table = None
    selected_tools = []

    for step in steps:
        tool_name = step["tool"]
        tool_input = step["input"]
        selected_tools.append(tool_name)

        tool = agent.tools[tool_name]
        raw_output = tool.invoke({"question": tool_input})

        answer_text, sources = parse_tool_output(raw_output)
        all_sources.extend(sources)

        workflow.append(TOOL_DISPLAY_NAMES.get(tool_name, tool_name.title()))
        workflow += ["Retriever", "Vector Store", "LLM"]

        if tool_name == "compare" and comparison_table is None:
            comparison_table = extract_markdown_table(answer_text)

        answer_chunks.append(answer_text)

    workflow.append("Final Answer")

    seen = set()
    unique_sources = []
    for s in all_sources:
        key = (s["file"], s["page"])
        if key not in seen:
            seen.add(key)
            unique_sources.append(s)

    primary_tool = selected_tools[0] if selected_tools else "retrieve"

    if len(selected_tools) > 1:
        reason = " Then, ".join(
            PLANNER_REASONS.get(t, "the user's request required this tool.") for t in selected_tools
        )
    else:
        reason = PLANNER_REASONS.get(primary_tool, "Selected based on the user's request.")

    if answer_chunks:
        answer_text_final = "\n\n".join(answer_chunks)
    else:
        answer_text_final = "No answer was produced."

    return {
        "answer": answer_text_final,
        "sources": unique_sources,
        "planner": {
            "selected_tool": primary_tool,
            "tools_used": selected_tools if selected_tools else [primary_tool],
            "reason": reason,
        },
        "workflow": workflow,
        "comparison_table": comparison_table,
    }


# ======================================================================
# SESSION STATE
# ======================================================================

DEFAULTS = {
    "question_input": "",
    "response": None,
    "error": None,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

EXAMPLE_QUESTIONS = [
    "What is Deep Learning?",
    "What is Gradient Descent?",
    "Summarize Neural Networks",
    "Summarize Gradient Descent",
    "Compare for loop and while loop ",
    "Create a quiz about Python",
    "Create a quiz about Neural Networks",
]


def set_question(text: str):
    st.session_state["question_input"] = text


def clear_all():
    st.session_state["question_input"] = ""
    st.session_state["response"] = None
    st.session_state["error"] = None


def ask(question: str):
    question = question.strip()
    if not question:
        st.session_state["error"] = "Please enter a question first."
        st.session_state["response"] = None
        return

    with st.spinner("🧠 Thinking..."):
        try:
            st.session_state["response"] = get_agent_response(question)
            st.session_state["error"] = None
        except Exception:
            st.session_state["response"] = None
            st.session_state["error"] = traceback.format_exc()


# ======================================================================
# UI SECTIONS
# ======================================================================

def render_header():
    st.markdown(
        """
        <div class="app-header">
            <div class="app-title">🎓 Course QA Agent</div>
            <div class="app-subtitle">
                Ask questions about the available course materials using an Agentic RAG system.
            </div>
        </div>
        <div class="badge-row">
            <span class="badge">🐍 Python</span>
            <span class="badge">🤖 Artificial Intelligence</span>
            <span class="badge">🧠 Machine Learning</span>
            <span class="badge">🔥 Deep Learning</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎓 Course QA Agent</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">Agentic RAG over your course materials</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-title">Supported Courses</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <span class="sidebar-chip">🐍 Python</span>
            <span class="sidebar-chip">🤖 AI</span>
            <span class="sidebar-chip">🧠 Machine Learning</span>
            <span class="sidebar-chip">🔥 Deep Learning</span>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section-title">Supported Tools</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sidebar-tool">✅ Retrieval</div>
            <div class="sidebar-tool">✅ Summary</div>
            <div class="sidebar-tool">✅ Compare</div>
            <div class="sidebar-tool">✅ Quiz</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="sidebar-section-title">Backend</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="sidebar-stack">
                LangChain<br>
                FAISS<br>
                Sentence Transformers<br>
                Groq<br>
                Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_examples():
    st.markdown('<div class="section-label">💡 Example Questions</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, example in enumerate(EXAMPLE_QUESTIONS):
        with cols[i % 2]:
            st.markdown('<div class="example-btn">', unsafe_allow_html=True)
            st.button(example, key=f"example_{i}", on_click=set_question, args=(example,))
            st.markdown('</div>', unsafe_allow_html=True)


def render_question_input():
    st.markdown('<div class="section-label">Ask a Question</div>', unsafe_allow_html=True)
    st.text_area(
        label="Question",
        key="question_input",
        placeholder="Ask anything about the available courses...",
        height=120,
        label_visibility="collapsed",
    )

    col1, col2, _ = st.columns([1, 1, 4])
    with col1:
        st.button("Ask", type="primary", use_container_width=True,
                   on_click=lambda: ask(st.session_state["question_input"]))
    with col2:
        st.button("Clear", use_container_width=True, on_click=clear_all)


def render_error():
    if st.session_state["error"]:
        st.markdown(
            f'<div class="error-card">⚠️ {st.session_state["error"].splitlines()[-1] if len(st.session_state["error"]) > 300 else st.session_state["error"]}</div>',
            unsafe_allow_html=True,
        )


def render_workflow(workflow):
    if not workflow:
        return
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 Agent Workflow</div>', unsafe_allow_html=True)

    html_parts = ['<div class="workflow-wrap">']
    for i, step in enumerate(workflow):
        css_class = "workflow-step final" if step == "Final Answer" else "workflow-step"
        html_parts.append(f'<span class="{css_class}">{step}</span>')
        if i < len(workflow) - 1:
            html_parts.append('<span class="workflow-arrow">→</span>')
    html_parts.append('</div>')

    st.markdown("".join(html_parts), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_planner_decision(planner):
    if not planner:
        return

    tools_used = planner.get("tools_used") or [planner.get("selected_tool", "")]
    label_title = "Selected Tools" if len(tools_used) > 1 else "Selected Tool"

    tool_badges = "".join(
        f'<span class="planner-value" style="margin-right:0.4rem;">{TOOL_DISPLAY_NAMES.get(t, str(t).title())}</span>'
        for t in tools_used
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧭 Planner Decision</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="planner-row">
            <div class="planner-item">
                <div class="section-label" style="margin-bottom:0;">{label_title}</div>
                <div>{tool_badges}</div>
            </div>
            <div class="planner-item">
                <div class="section-label" style="margin-bottom:0;">Reason</div>
                <div class="planner-reason">{planner.get("reason", "")}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_comparison_table(table_rows):
    import pandas as pd

    # Still built as a real DataFrame (for structure / potential export),
    # but rendered as HTML so markdown bold and <br> line breaks inside
    # cells actually render, and long text wraps instead of truncating.
    df = pd.DataFrame(table_rows)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Comparison</div>', unsafe_allow_html=True)

    headers_html = "".join(
        f"<th>{md_bold_to_html(str(col))}</th>" for col in df.columns
    )

    rows_html = ""
    for _, row in df.iterrows():
        cells_html = "".join(
            f"<td>{md_bold_to_html(str(val))}</td>" for val in row
        )
        rows_html += f"<tr>{cells_html}</tr>"

    st.markdown(
        f"""
        <div class="comparison-wrap">
            <table class="comparison-table">
                <thead><tr>{headers_html}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_answer(answer_text):
    if answer_text:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🤖 Answer</div>', unsafe_allow_html=True)
        st.markdown(answer_text)
        st.markdown('</div>', unsafe_allow_html=True)


def render_sources(sources):
    if not sources:
        return
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📚 Sources</div>', unsafe_allow_html=True)

    for src in sources:
        page_html = f'<span class="src-page">Page {src["page"]}</span>' if src.get("page") is not None else ""
        st.markdown(
            f"""
            <div class="source-card">
                <span class="src-icon">📄</span>
                <span>{src["file"]}</span>
                {page_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    st.markdown(
        """
        <div class="app-footer">
            Built with <b>Agentic RAG</b><br>
            Planner → Tool → Retriever → Vector Store → LLM
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================================================================
# APP LAYOUT
# ======================================================================

render_sidebar()
render_header()
render_question_input()
render_examples()

st.markdown("<br>", unsafe_allow_html=True)

render_error()

response = st.session_state["response"]
if response:
    render_answer(answer_text=response["answer"])
    render_sources(response["sources"])
    render_workflow(response["workflow"])
    render_planner_decision(response["planner"])

render_footer()