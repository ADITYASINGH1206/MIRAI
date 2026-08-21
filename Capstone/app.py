import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page settings — sidebar expanded to match Stitch left nav
st.set_page_config(
    page_title="STUDY OS // Precision Learning Platform",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# ═══════════════════════════════════════════════════════
#  STITCH "CINEMATIC PRECISION" DESIGN SYSTEM — FULL CSS
# ═══════════════════════════════════════════════════════

def inject_theme():
    # Dynamic Theme Injection
    is_light = st.session_state.get("theme", "Dark") == "Light"
    
    # Palette
    bg = "#F9FAFB" if is_light else "#070708"
    sidebar_bg = "#FFFFFF" if is_light else "#0d0e0f"
    text = "#111827" if is_light else "#e5e2e3"
    text_muted = "#6B7280" if is_light else "#9A9DA3"
    border = "rgba(0,0,0,0.1)" if is_light else "#232426"
    panel_bg = "rgba(255, 255, 255, 0.92)" if is_light else "rgba(13, 14, 15, 0.92)"
    hover_bg = "rgba(0,0,0,0.04)" if is_light else "rgba(255,255,255,0.04)"
    btn_bg = "#F3F4F6" if is_light else "#191A1C"
    btn_hover_bg = "#E5E7EB" if is_light else "#232426"
    accent = "#2563EB" if is_light else "#5E6BFF"
    accent_text = "#1D4ED8" if is_light else "#bec2ff"
    
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&display=swap');

    #MainMenu, header, footer, [data-testid="stToolbar"] {{visibility: hidden !important; height: 0 !important;}}
    .block-container {{
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 1400px !important;
    }}

    .stApp {{
        background-color: {bg} !important;
        font-family: 'Inter', sans-serif !important;
        color: {text} !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
        width: 260px !important;
        min-width: 260px !important;
    }}
    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1.25rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }}
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        background-color: {sidebar_bg} !important;
    }}

    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.04em !important;
        color: {text} !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border: 1px solid {border} !important;
        border-radius: 4px !important;
        background: {panel_bg} !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06) !important;
        padding: 16px !important;
        transition: border-color 0.2s ease !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: rgba(94, 107, 255, 0.4) !important;
    }}

    .stButton > button {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        background: {btn_bg} !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        background: {btn_hover_bg} !important;
        border-color: {accent} !important;
    }}

    [data-testid="stFormSubmitButton"] > button {{
        background: {text} !important;
        border: none !important;
        color: {bg} !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
    }}
    [data-testid="stFormSubmitButton"] > button:hover {{
        background: {accent} !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stMetric"] {{
        background: {panel_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 4px !important;
        padding: 14px 16px !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.68rem !important;
        text-transform: uppercase !important;
        color: {text_muted} !important;
        letter-spacing: 0.04em !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
        color: {text} !important;
        letter-spacing: -0.03em !important;
    }}

    .stTextInput input, .stTextArea textarea {{
        background: {btn_bg} !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        font-family: 'Inter', sans-serif !important;
        border-radius: 4px !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 1px {accent} !important;
    }}

    .stRadio > div {{ gap: 6px !important; }}
    .stRadio label {{
        background: {sidebar_bg} !important;
        border: 1px solid {border} !important;
        border-radius: 4px !important;
        padding: 10px 14px !important;
        color: {text} !important;
        font-size: 0.88rem !important;
        transition: all 0.15s ease !important;
    }}
    .stRadio label:hover {{ border-color: {accent} !important; }}

    .streamlit-expanderHeader {{
        background: transparent !important;
        border: none !important;
        color: {text_muted} !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
    }}

    .heatmap-cell {{
        width: 12px; height: 12px;
        border-radius: 2px;
        background-color: {btn_bg};
        border: 1px solid {border};
        display: inline-block;
    }}
    .heatmap-cell.level-1 {{ background-color: rgba(94, 107, 255, 0.2); }}
    .heatmap-cell.level-2 {{ background-color: rgba(94, 107, 255, 0.4); }}
    .heatmap-cell.level-3 {{ background-color: rgba(94, 107, 255, 0.7); }}
    .heatmap-cell.level-4 {{ background-color: {accent}; }}

    .quiz-correct {{
        background: rgba(16,185,129,0.08) !important;
        border: 1px solid rgba(16,185,129,0.3) !important;
        border-radius: 4px; padding: 12px 14px; margin-top: 8px; color: #10B981;
    }}
    .quiz-incorrect {{
        background: rgba(239,68,68,0.08) !important;
        border: 1px solid rgba(239,68,68,0.3) !important;
        border-radius: 4px; padding: 12px 14px; margin-top: 8px; color: #EF4444;
    }}

    .mono-telemetry {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.68rem !important; font-weight: 600 !important;
        text-transform: uppercase !important; letter-spacing: 0.15em !important;
        color: {text_muted} !important;
    }}
    .fig-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.12em;
        color: {text_muted}; margin-bottom: 12px;
    }}
    .stitch-card {{
        background: {panel_bg};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
        transition: border-color 0.2s ease;
    }}
    .accent-text {{ color: {accent_text}; }}
    .cyan-text {{ color: #0ea5e9; }}
    
    /* Custom Sidebar Nav via HTML */
    .sb-nav-item {{
        display: flex; align-items: center; gap: 10px;
        color: {text_muted}; text-decoration: none;
        font-family: 'Inter', sans-serif; font-size: 0.88rem;
        padding: 10px 12px; border-radius: 6px; margin: 2px 0;
        transition: all 0.15s ease;
    }}
    .sb-nav-item:hover {{
        background: {hover_bg}; color: {text};
    }}
    .sb-nav-active {{
        background: rgba(94,107,255,0.08);
        border-right: 3px solid {accent};
        color: {accent_text}; font-weight: 500;
    }}
    .sb-nav-item svg {{
        width: 16px; height: 16px; flex-shrink: 0;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  ACTIVITY LOGGING & MOCK DATA
# ═══════════════════════════════════════════════════════
def generate_mock_activity_log():
    activities = ["Flashcard", "Quiz", "Roadmap", "Deep Dive"]
    topics = ["Data Science", "Web Security", "Competitive Programming"]
    rows = []
    base_date = datetime.now().date()
    np.random.seed(42)
    for i in range(45, 0, -1):
        d = base_date - timedelta(days=i)
        n = np.random.choice([1, 2, 3, 4, 5], p=[0.2, 0.3, 0.25, 0.15, 0.1])
        for _ in range(n):
            rows.append({
                "Date": d.strftime("%Y-%m-%d"),
                "Activity_Type": np.random.choice(activities),
                "Topic": np.random.choice(topics),
                "Mastery_Score": np.random.randint(65, 100)
            })
    return pd.DataFrame(rows)


def log_activity(activity_type, topic="General", mastery_score=85):
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = generate_mock_activity_log()
    new_entry = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Activity_Type": activity_type,
        "Topic": topic,
        "Mastery_Score": mastery_score
    }])
    st.session_state.activity_log = pd.concat([st.session_state.activity_log, new_entry], ignore_index=True)


# ═══════════════════════════════════════════════════════
#  STATE MANAGEMENT & DEFAULTS
# ═══════════════════════════════════════════════════════
def init_state():
    query_page = st.query_params.get("page")
    if query_page:
        st.session_state.current_page = query_page
    elif "current_page" not in st.session_state:
        st.session_state.current_page = "explain"


    if "activity_log" not in st.session_state:
        st.session_state.activity_log = generate_mock_activity_log()

    # Prerequisite Roadmap
    if "mermaid_code" not in st.session_state:
        st.session_state.mermaid_code = """graph TD
    A[Theory of Computation] --> B[Formal Languages & Grammars]
    A --> C[Automata Theory & Turing Machines]
    B --> D[Syntax & Semantics Parsing]
    C --> E[Decidability & Complexity Classes P vs NP]
    D --> F[Static Code Analysis & AST Parsing]
    E --> G[Model Checking & Formal Verification]
    F --> H[Software Engineering Testing Models]
    G --> H
    H --> I[Unit, Integration & Mutation Testing]
    H --> J[Fuzzing & Security Test Suites]

    classDef default fill:#101112,stroke:#232426,stroke-width:1.5px,color:#e5e2e3;
    classDef startNode fill:#191A1C,stroke:#5E6BFF,stroke-width:2px,color:#ffffff;
    classDef targetNode fill:#151618,stroke:#50d8e9,stroke-width:2px,color:#ffffff;
    class A startNode;
    class H targetNode;"""

    # Sticky Notes
    if "sticky_notes" not in st.session_state:
        st.session_state.sticky_notes = [
            "IDS (Intrusion Detection System) operates out-of-band via TAP/SPAN port mirroring. It monitors and alerts on suspicious traffic without blocking packets inline.",
            "IPS (Intrusion Prevention System) sits directly inline with network traffic. It actively inspects packets in real-time and drops malicious flows before reaching hosts.",
            "Signature-Based vs Anomaly-Based: Both systems can use known attack signatures or statistical baseline heuristics to identify zero-day exploits.",
            "Key Architectural Difference: IDS failure maintains network availability (fail-open), whereas IPS inline failure could disrupt network connectivity (fail-closed)."
        ]

    # Explain & Memorize
    if "explain_topic" not in st.session_state:
        st.session_state.explain_topic = "Supervised vs. Unsupervised Learning"
        st.session_state.explanation_text = "Supervised learning trains algorithms on labeled datasets where each input has a corresponding ground-truth target label, enabling the model to learn mapping functions for classification and regression. Unsupervised learning analyzes unlabeled datasets without human intervention to discover latent representations, cluster structures, and dimensional distributions."
        st.session_state.explain_flashcards = [
            {"q": "What is the primary distinguishing characteristic of Supervised Learning?", "a": "Models are trained on labeled pairs of inputs and target outputs (ground truth)."},
            {"q": "Name two primary unsupervised learning algorithmic tasks.", "a": "Clustering (e.g., K-Means, DBSCAN) and Dimensionality Reduction (e.g., PCA, t-SNE)."},
            {"q": "What loss formulation is commonly minimized in Supervised Regression?", "a": "Mean Squared Error (MSE) empirical loss."},
            {"q": "How does PCA achieve unsupervised dimensionality reduction?", "a": "By projecting data onto orthogonal eigenvectors of the covariance matrix with maximum variance."},
            {"q": "What is semi-supervised learning?", "a": "A hybrid paradigm leveraging a small subset of labeled data alongside a large pool of unlabeled samples."}
        ]

    # Quiz Builder
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = [
            {"question": "Where is an Intrusion Prevention System (IPS) deployed within a network topology?",
             "options": ["Out-of-band via SPAN/Mirror port", "Directly in-line with network traffic", "Exclusively on DNS root servers", "Inside end-user browser storage"],
             "answer": "Directly in-line with network traffic",
             "explanation": "An IPS must sit directly in the traffic pathway (in-line) to inspect, drop, or rewrite malicious packets."},
            {"question": "What is the key functional difference between an IDS and an IPS?",
             "options": ["IDS detects and alerts; IPS detects and actively drops packets", "IDS operates only on Layer 2; IPS on Layer 7", "IDS encrypts traffic; IPS decrypts traffic", "There is no difference; they are synonymous"],
             "answer": "IDS detects and alerts; IPS detects and actively drops packets",
             "explanation": "IDS is a passive detection and telemetry alerting system, while IPS is active preventative enforcement."},
            {"question": "Which fail-state behavior is typical when an in-line IPS crashes without bypass hardware?",
             "options": ["Fail-Open (All traffic passes)", "Fail-Closed (Network traffic blocked)", "Automatic DNS sinkholing", "Instant conversion to IDS mode"],
             "answer": "Fail-Closed (Network traffic blocked)",
             "explanation": "Without specialized bypass NICs, an in-line device crash severs the physical/logical link."},
            {"question": "How does Signature-Based Detection differ from Anomaly-Based Detection?",
             "options": ["Signatures match known byte patterns; Anomaly detects deviation from baseline statistical norms", "Signature detection requires AI; Anomaly uses static regex", "Signatures work only on encrypted packets", "Anomaly detection cannot identify zero-day vulnerabilities"],
             "answer": "Signatures match known byte patterns; Anomaly detects deviation from baseline statistical norms",
             "explanation": "Signature engines inspect known CVE strings/byte sequences, anomaly engines detect unusual volumetric spikes."},
            {"question": "Which network component is typically used to feed telemetry to a passive IDS?",
             "options": ["Network TAP or Switch SPAN/Mirror Port", "DHCP Option 82 Relay", "BGP Autonomous System Boundary Router", "RADIUS Accounting Agent"],
             "answer": "Network TAP or Switch SPAN/Mirror Port",
             "explanation": "TAPs and SPAN/mirror ports copy packets out-of-band to the IDS without impacting active forwarding."}
        ]
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

    # Deep Dive Revision Notes
    if "revision_notes" not in st.session_state:
        st.session_state.revision_notes = """# Core Paradigm: Supervised vs. Unsupervised Learning

| Dimension | Supervised Learning | Unsupervised Learning |
| :--- | :--- | :--- |
| **Training Data** | Labeled pairs $\\{(x_i, y_i)\\}$ | Unlabeled inputs $\\{x_i\\}$ |
| **Objective** | Minimize empirical risk | Discover latent structure |
| **Primary Tasks** | Classification, Regression | Clustering, Dim. Reduction |
| **Evaluation** | Accuracy, F1, MSE | Silhouette, DB Index |
"""

init_state()


# ═══════════════════════════════════════════════════════
#  AI SYNTHESIS PIPELINES
# ═══════════════════════════════════════════════════════
def run_explain_pipeline(topic_query):
    if not API_KEY:
        st.error("Gemini API key is not configured.")
        return False
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""You are an expert AI Educator. Explain the topic: "{topic_query}".
Return a strictly valid JSON object with:
1. "explanation": A concise, clear explanation (2-3 paragraphs).
2. "flashcards": An array of exactly 5 Q&A objects ({{"q": "...", "a": "..."}}).
Output ONLY raw JSON."""
        res = model.generate_content(prompt)
        text = res.text.strip()
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        data = json.loads(text.strip())
        st.session_state.explain_topic = topic_query
        st.session_state.explanation_text = data.get("explanation", "")
        st.session_state.explain_flashcards = data.get("flashcards", [])[:5]
        log_activity("Flashcard", topic=topic_query, mastery_score=90)
        return True
    except Exception as e:
        st.error(f"Error generating explanation: {e}")
        return False


def run_quiz_builder_pipeline(raw_content):
    if not API_KEY:
        st.error("Gemini API key is not configured.")
        return False
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""Analyze the following study material and generate a 5-question multiple choice quiz:
\"\"\"{raw_content}\"\"\"
Output a strictly valid JSON array of 5 objects, each with:
- "question": string
- "options": array of exactly 4 strings
- "answer": string (exact match to one option)
- "explanation": string
Output ONLY raw JSON."""
        res = model.generate_content(prompt)
        text = res.text.strip()
        if text.startswith("```json"): text = text[7:]
        if text.startswith("```"): text = text[3:]
        if text.endswith("```"): text = text[:-3]
        data = json.loads(text.strip())
        if isinstance(data, dict) and "quiz" in data:
            data = data["quiz"]
        st.session_state.quiz_data = data[:5]
        st.session_state.quiz_submitted = False
        log_activity("Quiz", topic="Custom Quiz", mastery_score=80)
        return True
    except Exception as e:
        st.error(f"Error generating quiz: {e}")
        return False


def run_study_os_pipeline(context_text, audio_stream=None, image_stream=None):
    if not API_KEY:
        st.error("Gemini API key is not configured in .env.")
        return False
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = """You are the Study OS Multimodal AI Engine.
Analyze the user's input context and generate a complete JSON payload:
{"mermaid": "graph TD\\n  A[...] --> B[...]\\n  ...",
 "sticky_notes": ["fact1","fact2","fact3","fact4"],
 "revision_notes": "# Markdown Study Guide\\n..."}
Output raw JSON only."""
        contents = [prompt]
        if context_text and context_text.strip():
            contents.append(f"Context:\n{context_text.strip()}")
        if image_stream:
            contents.append({"mime_type": "image/jpeg", "data": image_stream.getvalue()})
        if audio_stream:
            contents.append({"mime_type": "audio/wav", "data": audio_stream.getvalue()})
        response = model.generate_content(contents)
        raw_text = response.text.strip()
        if raw_text.startswith("```json"): raw_text = raw_text[7:]
        elif raw_text.startswith("```"): raw_text = raw_text[3:]
        if raw_text.endswith("```"): raw_text = raw_text[:-3]
        payload = json.loads(raw_text.strip())
        if "mermaid" in payload and payload["mermaid"]:
            st.session_state.mermaid_code = payload["mermaid"].strip()
        if "sticky_notes" in payload and isinstance(payload["sticky_notes"], list) and len(payload["sticky_notes"]) >= 4:
            st.session_state.sticky_notes = payload["sticky_notes"][:4]
        if "revision_notes" in payload and payload["revision_notes"]:
            st.session_state.revision_notes = payload["revision_notes"]
        log_activity("Roadmap", topic="Master Ingestion", mastery_score=95)
        return True
    except Exception as e:
        st.error(f"Error during AI pipeline execution: {e}")
        return False


# ═══════════════════════════════════════════════════════
#  STITCH LEFT SIDEBAR — Exact replica of SideNavBar
# ═══════════════════════════════════════════════════════
with st.sidebar:
    # Theme Toggle
    theme_choice = st.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.get("theme", "Dark") == "Dark" else 1, horizontal=True, label_visibility="collapsed")
    if theme_choice != st.session_state.get("theme", "Dark"):
        st.session_state.theme = theme_choice
        st.rerun()

    # Brand block
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding:4px 8px; margin-bottom:12px;">
            <div style="width:30px;height:30px;background:{'#F3F4F6' if theme_choice == 'Light' else '#191A1C'};border:1px solid {'rgba(0,0,0,0.1)' if theme_choice == 'Light' else '#232426'};border-radius:50%;display:flex;align-items:center;justify-content:center;">
                <span style="font-family:'Manrope';font-weight:800;color:{'#1D4ED8' if theme_choice == 'Light' else '#bec2ff'};font-size:13px;">S</span>
            </div>
            <div>
                <div style="font-family:'Manrope';font-weight:700;font-size:1.05rem;letter-spacing:-0.04em;color:{'#111827' if theme_choice == 'Light' else '#FFFFFF'};">STUDY OS</div>
                <div style="font-family:'JetBrains Mono';font-size:0.6rem;color:{'#6B7280' if theme_choice == 'Light' else '#9A9DA3'};letter-spacing:0.15em;text-transform:uppercase;">Precision Learning</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # NEW WORKSPACE button
    st.markdown(f"""
        <div style="padding:0 4px; margin-bottom:16px;">
            <div style="background:{'#111827' if theme_choice == 'Light' else '#e5e2e3'};color:{'#FFFFFF' if theme_choice == 'Light' else '#070708'};font-family:'JetBrains Mono';font-size:0.7rem;font-weight:700;
                        text-align:center;padding:8px;border-radius:4px;text-transform:uppercase;letter-spacing:0.08em;
                        cursor:pointer;">
                + New Workspace
            </div>
        </div>
    """, unsafe_allow_html=True)

    svg_brain = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/></svg>'
    svg_pen = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>'
    svg_chart = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>'
    
    current_page = st.session_state.current_page
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; gap:2px;">
            <a href="?page=explain" target="_self" class="sb-nav-item {'sb-nav-active' if current_page == 'explain' else ''}">
                {svg_brain} Explain & Memorize
            </a>
            <a href="?page=quiz" target="_self" class="sb-nav-item {'sb-nav-active' if current_page == 'quiz' else ''}">
                {svg_pen} Quiz Builder
            </a>
            <a href="?page=analytics" target="_self" class="sb-nav-item {'sb-nav-active' if current_page == 'analytics' else ''}">
                {svg_chart} Analytics & Roadmap
            </a>
        </div>
    """, unsafe_allow_html=True)

    # Spacer then bottom links
    st.markdown("<div style='flex:1;min-height:200px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="border-top:1px solid {'rgba(0,0,0,0.1)' if theme_choice == 'Light' else '#232426'};padding-top:12px;margin-top:12px;">
            <div style="padding:8px 12px;color:{'#6B7280' if theme_choice == 'Light' else '#9A9DA3'};font-family:'JetBrains Mono';font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px;vertical-align:middle"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg> Settings
            </div>
            <div style="padding:8px 12px;color:{'#6B7280' if theme_choice == 'Light' else '#9A9DA3'};font-family:'JetBrains Mono';font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right:6px;vertical-align:middle"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/></svg> Support
            </div>
        </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  TOP APP BAR — Stitch header
# ═══════════════════════════════════════════════════════
active_tab_map = {"explain": "Flashcards", "quiz": "Flashcards", "analytics": "Performance"}
active_tab = active_tab_map.get(st.session_state.current_page, "Dashboard")

def tab_style(name):
    if name == active_tab:
        return "color:#bec2ff;border-bottom:2px solid #5E6BFF;padding-bottom:4px;"
    return "color:#9A9DA3;"

st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #232426;padding-bottom:10px;margin-bottom:24px;">
        <div style="display:flex;gap:20px;font-family:'JetBrains Mono';font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;">
            <span style="{tab_style('Dashboard')}">Dashboard</span>
            <span style="{tab_style('Flashcards')}">Flashcards</span>
            <span style="{tab_style('Performance')}">Performance</span>
        </div>
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="background:#1a1b1d;border:1px solid #232426;padding:4px 10px;border-radius:4px;font-family:'JetBrains Mono';font-size:0.68rem;color:#9A9DA3;">
                Search parameters...
            </div>
            <span style="color:#9A9DA3;font-size:1.1rem;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg></span>
            <span style="color:#9A9DA3;font-size:1.1rem;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span>
        </div>
    </div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE: EXPLAIN & MEMORIZE
# ═══════════════════════════════════════════════════════
if st.session_state.current_page == "explain":
    # System Input bar
    st.markdown("<div class='fig-label'>● System Input</div>", unsafe_allow_html=True)

    with st.form("explain_form"):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            topic_input = st.text_input(
                "Topic", value=st.session_state.explain_topic,
                placeholder="e.g. Supervised vs. Unsupervised Learning",
                label_visibility="collapsed"
            )
        with col_btn:
            explain_submit = st.form_submit_button("EXECUTE ⌘")

    if explain_submit and topic_input:
        with st.spinner("Synthesizing concept..."):
            if run_explain_pipeline(topic_input):
                st.rerun()

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # FIG 1.0 // Comparative Analysis — two-column explanation
    st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span class="fig-label">FIG 1.0 // Comparative Analysis</span>
            <span style="font-family:'JetBrains Mono';font-size:0.62rem;color:#50d8e9;">◆ Confidence: High</span>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""
            <div style="padding:4px;">
                <h3 style="font-size:1.3rem;margin-bottom:12px;color:#bec2ff;">{st.session_state.explain_topic}</h3>
                <p style="color:#c4c1c2;font-size:0.92rem;line-height:1.65;">{st.session_state.explanation_text}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Memory Vectors — flashcards grid
    st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span class="fig-label">Memory Vectors [{len(st.session_state.explain_flashcards)}]</span>
        </div>
    """, unsafe_allow_html=True)

    card_cols = st.columns(min(len(st.session_state.explain_flashcards), 3), gap="medium")
    for idx, card in enumerate(st.session_state.explain_flashcards[:3]):
        with card_cols[idx]:
            with st.container():
                st.markdown(f"""
                    <div class="fig-label" style="color:#50d8e9;">CARD.{idx+1:02d}</div>
                    <h4 style="font-size:1rem;margin-bottom:6px;">{card['q'].split('?')[0].split('.')[-1].strip()[:40]}</h4>
                    <p style="color:#9A9DA3;font-size:0.82rem;line-height:1.5;">{card['a'][:100]}</p>
                """, unsafe_allow_html=True)

    # Show remaining cards
    if len(st.session_state.explain_flashcards) > 3:
        card_cols2 = st.columns(min(len(st.session_state.explain_flashcards) - 3, 3), gap="medium")
        for idx, card in enumerate(st.session_state.explain_flashcards[3:]):
            with card_cols2[idx]:
                with st.container():
                    st.markdown(f"""
                        <div class="fig-label" style="color:#50d8e9;">CARD.{idx+4:02d}</div>
                        <h4 style="font-size:1rem;margin-bottom:6px;">{card['q'].split('?')[0].split('.')[-1].strip()[:40]}</h4>
                        <p style="color:#9A9DA3;font-size:0.82rem;line-height:1.5;">{card['a'][:100]}</p>
                    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE: QUIZ BUILDER
# ═══════════════════════════════════════════════════════
elif st.session_state.current_page == "quiz":
    st.markdown("""
        <div style="margin-bottom:4px;">
            <span style="font-family:'JetBrains Mono';font-size:0.68rem;color:#50d8e9;text-transform:uppercase;letter-spacing:0.12em;">◆ Module: Network Security</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("## Knowledge Extraction")

    # Two-panel layout matching Stitch screenshot
    quiz_left, quiz_right = st.columns([1, 1.2], gap="medium")

    with quiz_left:
        # FIG 1 // Source Telemetry
        st.markdown("<div class='fig-label'>FIG. 1 // Source Telemetry</div>", unsafe_allow_html=True)
        with st.container():
            with st.form("quiz_gen_form"):
                raw_text_input = st.text_area(
                    "Source",
                    placeholder="Inject unstructured lecture notes or technical\ndocumentation here for algorithmic parsing.\n\n> Routing data input sequences...\n> Parse content regarding: Network Security, IDS, IPS,\n  Firewalls, etc.",
                    height=280,
                    label_visibility="collapsed"
                )
                gen_quiz_btn = st.form_submit_button("EXECUTE PARSER ⌘", use_container_width=True)

            if gen_quiz_btn and raw_text_input:
                with st.spinner("Analyzing text and constructing evaluation..."):
                    if run_quiz_builder_pipeline(raw_text_input):
                        st.rerun()

    with quiz_right:
        # FIG 2 // Evaluation Matrix
        st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span class="fig-label">FIG. 2 // Evaluation Matrix</span>
                <div style="display:flex;gap:12px;">
                    <span style="font-family:'JetBrains Mono';font-size:0.62rem;color:#9A9DA3;">Q:1D, 5xMPAA</span>
                    <span style="font-family:'JetBrains Mono';font-size:0.62rem;color:#9A9DA3;">DIFF: HARD</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.form("quiz_eval_form"):
            user_answers = {}
            for q_idx, q_item in enumerate(st.session_state.quiz_data):
                if q_idx == 0:
                    # Show first question prominently
                    st.markdown(f"<h3 style='font-size:1.1rem;line-height:1.4;margin-bottom:12px;'>{q_item['question']}</h3>", unsafe_allow_html=True)
                    st.markdown("<hr style='border-color:#232426;margin:8px 0 12px 0;'>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**Q{q_idx+1}: {q_item['question']}**")

                user_answers[q_idx] = st.radio(
                    f"Q{q_idx+1}", options=q_item["options"],
                    key=f"quiz_opt_{q_idx}", label_visibility="collapsed"
                )
                if q_idx < len(st.session_state.quiz_data) - 1:
                    st.markdown("<hr style='border-color:#232426;margin:10px 0;'>", unsafe_allow_html=True)

            submit_quiz = st.form_submit_button("SUBMIT EVALUATION", use_container_width=True)

        if submit_quiz:
            st.session_state.quiz_submitted = True
            correct_count = sum(1 for i, q in enumerate(st.session_state.quiz_data) if user_answers[i] == q["answer"])
            st.session_state.quiz_score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            log_activity("Quiz", topic="Quiz Submission", mastery_score=st.session_state.quiz_score)

        if st.session_state.get("quiz_submitted", False):
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="stitch-card" style="text-align:center;padding:16px;">
                    <div class="fig-label">Evaluation Result</div>
                    <div style="font-family:'Manrope';font-size:2.5rem;font-weight:800;color:{'#6EE7B7' if st.session_state.quiz_score >= 70 else '#FCA5A5'};">
                        {st.session_state.quiz_score}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

            for q_idx, q_item in enumerate(st.session_state.quiz_data):
                user_ans = user_answers.get(q_idx, "")
                is_correct = user_ans == q_item["answer"]
                css_class = "quiz-correct" if is_correct else "quiz-incorrect"
                st.markdown(f"""
                    <div class="{css_class}">
                        <b>Q{q_idx+1}: {'✓ Correct' if is_correct else '✗ Incorrect'}</b><br>
                        {'<b>Correct:</b> ' + q_item['answer'] + '<br>' if not is_correct else ''}
                        <i>{q_item['explanation']}</i>
                    </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
#  PAGE: ANALYTICS & ROADMAP
# ═══════════════════════════════════════════════════════
elif st.session_state.current_page == "analytics":
    # Page header matching Stitch
    head_left, head_right = st.columns([3, 1])
    with head_left:
        st.markdown("## System Analytics")
        st.markdown("<div class='mono-telemetry'>Runtime: 142h 34m | Status: Nominal</div>", unsafe_allow_html=True)
    with head_right:
        st.markdown("""
            <div style="text-align:right;padding-top:8px;">
                <span style="background:#1a1b1d;border:1px solid #232426;padding:5px 10px;border-radius:4px;
                             font-family:'JetBrains Mono';font-size:0.7rem;color:#bec2ff;cursor:pointer;">
                    ↓ Export
                </span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # 3 KPI Cards — FIG 1, 2, 3
    df_act = st.session_state.activity_log
    total_activities = len(df_act)
    avg_retention = int(df_act["Mastery_Score"].mean()) if not df_act.empty else 94
    unique_days = df_act["Date"].nunique() if not df_act.empty else 42

    kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
    with kpi1:
        st.metric("Cards Mastered", f"{total_activities * 28:,}", delta="+12% vs last week")
    with kpi2:
        st.metric("Current Streak", f"{unique_days} Days", delta="Optimal consistency")
    with kpi3:
        st.metric("Retention Rate", f"{avg_retention}.2%", delta="Target: 95%")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # FIG 4 // Activity Signal — Heatmap
    with st.container():
        st.markdown("<div class='fig-label'>FIG. 4 // Activity Signal</div>", unsafe_allow_html=True)

        daily_counts = df_act.groupby("Date").size().to_dict()
        today = datetime.now().date()
        start_date = today - timedelta(days=364)

        heatmap_html = '<div style="display:flex;gap:3px;overflow-x:auto;padding:4px 0;">'
        for week in range(52):
            heatmap_html += '<div style="display:flex;flex-direction:column;gap:3px;">'
            for day in range(7):
                cell_date = start_date + timedelta(days=week * 7 + day)
                count = daily_counts.get(cell_date.strftime("%Y-%m-%d"), 0)
                level = "" if count == 0 else f"level-{min(count, 4)}"
                heatmap_html += f'<div class="heatmap-cell {level}" title="{cell_date}: {count}"></div>'
            heatmap_html += '</div>'
        heatmap_html += '</div>'

        heatmap_html += """
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;">
            <span style="font-family:'JetBrains Mono';font-size:0.62rem;color:#9A9DA3;text-transform:uppercase;">Last 365 Days</span>
            <div style="display:flex;align-items:center;gap:4px;font-family:'JetBrains Mono';font-size:0.62rem;color:#9A9DA3;text-transform:uppercase;">
                <span>Less</span>
                <span class="heatmap-cell"></span>
                <span class="heatmap-cell level-1"></span>
                <span class="heatmap-cell level-2"></span>
                <span class="heatmap-cell level-3"></span>
                <span class="heatmap-cell level-4"></span>
                <span>More</span>
            </div>
        </div>
        """
        st.markdown(heatmap_html, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # FIG 5 // Knowledge Topology — Mermaid Roadmap
    with st.container():
        st.markdown("<div class='fig-label'>FIG. 5 // Knowledge Topology</div>", unsafe_allow_html=True)

        mermaid_html = f"""
        <!DOCTYPE html><html><head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
        <style>body{{margin:0;padding:12px;background:transparent;display:flex;justify-content:center;}}</style>
        </head><body>
        <div class="mermaid">{st.session_state.mermaid_code}</div>
        <script>mermaid.initialize({{startOnLoad:true,theme:'dark',themeVariables:{{
            darkMode:true,background:'#070708',primaryColor:'#101112',primaryTextColor:'#e5e2e3',
            primaryBorderColor:'#5E6BFF',lineColor:'#bec2ff',secondaryColor:'#191A1C',tertiaryColor:'#070708'
        }}}});</script></body></html>"""
        components.html(mermaid_html, height=380, scrolling=True)


# ═══════════════════════════════════════════════════════
#  MASTER INGESTION STREAM — always visible at bottom
# ═══════════════════════════════════════════════════════
st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
st.markdown("<div class='fig-label'>System // Multimodal Ingestion</div>", unsafe_allow_html=True)

with st.container():
    with st.form("master_input_form"):
        form_col1, form_col2 = st.columns([2.5, 1], gap="medium")
        with form_col1:
            input_text = st.text_area(
                "Lecture Transcript / Syllabus",
                placeholder="Inject lecture transcript, syllabus outline, or technical topics here...",
                height=100, label_visibility="collapsed"
            )
        with form_col2:
            input_audio = st.audio_input("Voice Dictation")
            input_camera = st.camera_input("Whiteboard Scan")
        submit_btn = st.form_submit_button("PROCESS & RESTRUCTURE", use_container_width=True)

    if submit_btn:
        if not (input_text or input_audio or input_camera):
            st.warning("Provide at least one input stream.")
        else:
            with st.spinner("Analyzing and compiling Study OS..."):
                success = run_study_os_pipeline(input_text, input_audio, input_camera)
                if success:
                    st.success("Study OS modules updated!")
                    st.rerun()
