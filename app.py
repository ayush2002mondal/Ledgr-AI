
import streamlit as st

from agent import run_agent
from planner import understand_task


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Ledgr",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------- CUSTOM STYLING ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp {
    background: #0b1020;
    color: #e8edf8;
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #f1f5ff;
}

.hero {
    background: linear-gradient(135deg, #151f3d, #10182d 65%, #172c50);
    border: 1px solid #263b65;
    border-radius: 22px;
    padding: 36px 40px;
    margin-bottom: 28px;
}

.hero-tag {
    color: #77a9ff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 42px;
    font-weight: 700;
    color: #f4f7ff;
    margin-top: 12px;
    line-height: 1.15;
}

.hero-subtitle {
    color: #aab8d4;
    font-size: 16px;
    margin-top: 12px;
    max-width: 650px;
    line-height: 1.7;
}

.section-label {
    color: #8ea6cf;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.panel {
    background: #121b30;
    border: 1px solid #263651;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
}

.step-number {
    display: inline-block;
    background: #1e3763;
    color: #83b3ff;
    border: 1px solid #34588d;
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 700;
    margin-right: 10px;
}

.status-pill {
    display: inline-block;
    background: #173b34;
    color: #75e0bb;
    border: 1px solid #286b59;
    padding: 6px 12px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 600;
}

div[data-testid="stTextInput"] input {
    background: #111c32;
    color: #f2f6ff;
    border: 1px solid #344968;
    border-radius: 12px;
    padding: 14px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #70a7ff;
    box-shadow: 0 0 0 1px #70a7ff;
}

.stButton > button {
    background: linear-gradient(135deg, #3979ed, #5a8fff);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 11px 22px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5590ff, #79a8ff);
    color: white;
    border: none;
    transform: translateY(-1px);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

div[data-testid="stJson"] {
    background: #101a2d;
    border: 1px solid #293c5a;
    border-radius: 12px;
}

hr {
    border-color: #263651;
}

.footer {
    text-align: center;
    color: #647694;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "task" not in st.session_state:
    st.session_state.task = None

if "result" not in st.session_state:
    st.session_state.result = None


# ---------------- HERO ----------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ Autonomous AI Workspace</div>
    <div class="hero-title">Ledgr AI</div>
    <div class="hero-subtitle">
        Your intelligent task assistant. Describe what you need in natural
        language, review the proposed actions, and let the AI execute and
        verify the work with your approval.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- TASK INPUT ----------------

st.markdown('<div class="section-label">01 / Create a task</div>',
            unsafe_allow_html=True)

st.markdown("### What can I help you with?")

user_request = st.text_input(
    "Task description",
    placeholder="e.g. Give me the latest bill from xyz company",
    label_visibility="collapsed"
)

st.caption("Try natural language. You don't need to use a fixed command format.")

col1, col2 = st.columns([1, 4])

with col1:
    understand_clicked = st.button(
        "✦ Understand Task",
        use_container_width=True
    )

if understand_clicked:

    if not user_request.strip():
        st.warning("Please describe a task first.")

    else:
        with st.spinner("AI is understanding your request..."):
            task = understand_task(user_request)

        if task["valid"]:
            st.session_state.task = task
            st.session_state.result = None
        else:
            st.session_state.task = None
            st.session_state.result = None
            st.error(task["message"])


# ---------------- TASK UNDERSTANDING ----------------

if st.session_state.task:

    task = st.session_state.task

    st.markdown("---")
    st.markdown('<div class="section-label">02 / AI interpretation</div>',
                unsafe_allow_html=True)

    st.markdown("### Here's what I understood")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.caption("DETECTED ACTION")
            st.markdown(f"### {task['action'].replace('_', ' ').title()}")

        with col2:
            st.caption("IDENTIFIED VENDOR")
            st.markdown(f"### {task['vendor']}")

    st.markdown("### Proposed execution plan")

    for i, step in enumerate(task["steps"], start=1):

        st.markdown(
            f"""
            <div class="panel" style="padding:16px 20px;">
                <span class="step-number">{i:02}</span>
                <span style="color:#e5edff;font-size:15px;">
                    {step}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown('<div class="section-label">03 / Human approval</div>',
                unsafe_allow_html=True)

    st.info(
        "The AI has prepared a plan. Nothing will be executed until you approve it."
    )

    if st.button("✓ Approve & Execute", use_container_width=True):

        with st.spinner("Ledgr is executing and verifying your task..."):

            result = run_agent(task["vendor"])

        st.session_state.result = result


# ---------------- EXECUTION RESULT ----------------

if st.session_state.result:

    result = st.session_state.result

    st.markdown("---")
    st.markdown('<div class="section-label">04 / Execution report</div>',
                unsafe_allow_html=True)

    st.markdown("### Agent activity")

    for log in result["logs"]:
        st.markdown(f"✓ {log}")

    if result["status"] == "completed":

        st.success("Task completed successfully.")

        st.markdown("### Verified invoice")

        invoice = result.get("invoice")

        if invoice:
            with st.container(border=True):

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.caption("VENDOR")
                    st.markdown(f"**{invoice.get('vendor', 'N/A')}**")

                with col2:
                    st.caption("INVOICE NUMBER")
                    st.markdown(f"**{invoice.get('invoice_number', 'N/A')}**")

                with col3:
                    st.caption("AMOUNT")
                    st.markdown(f"**₹{invoice.get('amount', 'N/A')}**")

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.caption("INVOICE DATE")
                    st.write(invoice.get("invoice_date", "N/A"))

                with col2:
                    st.caption("DUE DATE")
                    st.write(invoice.get("due_date", "N/A"))

                with st.expander("View complete invoice data"):
                    st.json(invoice)

    else:
        st.error(result["message"])


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    Ledgr AI
</div>
""", unsafe_allow_html=True)