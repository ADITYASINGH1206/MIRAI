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

# Configure page settings
st.set_page_config(
    page_title="STUDY OS // Precision Learning Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- CSS OVERRIDES & STITCH EXACT THEME INJECTION ---
def inject_theme():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* Nuke Streamlit default headers & footers */
    #MainMenu, header, footer {visibility: hidden !important;}
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1560px !important;
    }

    /* Stitch Palette: Deep Space & Cinematic Precision */
    .stApp {
        background-color: #070708 !important;
        background-image: 
            radial-gradient(circle at 50% 0%, rgba(94, 107, 255, 0.05) 0%, transparent 70%),
            radial-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 100% 100%, 20px 20px;
        font-family: 'Inter', sans-serif !important;
        color: #e5e2e3 !important;
    }

    /* Headings (Manrope 520 / Tight Tracking) */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.045em !important;
        color: #FFFFFF !important;
    }

    .hero-headline {
        font-family: 'Manrope', sans-serif !important;
        font-size: 4rem !important;
        font-weight: 800 !important;
        line-height: 1.05 !important;
        letter-spacing: -0.055em !important;
        background: linear-gradient(180deg, #FFFFFF 20%, #8f8fa1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.25rem !important;
    }

    .mono-telemetry {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
        color: #bec2ff !important;
    }

    /* Stitch Glass Panels & Low-Contrast Outlines */
    .stitch-glass-panel {
        background: rgba(16, 17, 18, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid #232426 !important;
        box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.08), 0 12px 32px rgba(0, 0, 0, 0.5) !important;
        border-radius: 6px !important;
        padding: 20px !important;
        position: relative !important;
        transition: all 0.25s ease !important;
    }

    .stitch-glass-panel:hover {
        border-color: #5E6BFF !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #232426 !important;
        border-radius: 6px !important;
        background-color: #101112 !important;
        padding: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #5E6BFF !important;
    }

    /* Stitch Tab Controllers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #101112;
        padding: 4px;
        border-radius: 6px;
        border: 1px solid #232426;
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #9A9DA3 !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        background: transparent !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background: rgba(94, 107, 255, 0.15) !important;
        border: 1px solid rgba(94, 107, 255, 0.4) !important;
        font-weight: 700 !important;
    }

    /* Primary & Secondary Buttons */
    .stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        background: #191A1C !important;
        border: 1px solid #232426 !important;
        color: #e5e2e3 !important;
        padding: 10px 20px !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #232426 !important;
        border-color: #5E6BFF !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(94, 107, 255, 0.2) !important;
    }

    [data-testid="stFormSubmitButton"] > button {
        background: #5E6BFF !important;
        border: 1px solid #bec2ff !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 20px rgba(94, 107, 255, 0.35) !important;
    }

    [data-testid="stFormSubmitButton"] > button:hover {
        background: #707CFF !important;
        border-color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(94, 107, 255, 0.5) !important;
    }

    /* KPI Metrics Styling */
    [data-testid="stMetric"] {
        background: #101112 !important;
        border: 1px solid #232426 !important;
        border-radius: 6px !important;
        padding: 16px 20px !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        color: #9A9DA3 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }

    /* Sticky Note & Flashcard Cards */
    .stitch-note-card {
        background: #151618 !important;
        border: 1px solid #232426 !important;
        border-top: 3px solid #5E6BFF !important;
        border-radius: 6px !important;
        padding: 18px !important;
        min-height: 170px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 16px !important;
        transition: all 0.25s ease !important;
    }

    .stitch-note-card:hover {
        transform: translateY(-4px) !important;
        border-color: #5E6BFF !important;
    }

    .stitch-note-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        color: #50d8e9;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .stitch-note-body {
        font-size: 0.9rem;
        line-height: 1.55;
        color: #e5e2e3;
    }

    /* Heatmap level styles */
    .heatmap-cell {
        width: 13px;
        height: 13px;
        border-radius: 2px;
        background-color: #1a1b1d;
        border: 1px solid #232426;
        display: inline-block;
    }
    .heatmap-cell.level-1 { background-color: rgba(190, 194, 255, 0.2); }
    .heatmap-cell.level-2 { background-color: rgba(190, 194, 255, 0.45); }
    .heatmap-cell.level-3 { background-color: rgba(94, 107, 255, 0.75); }
    .heatmap-cell.level-4 { background-color: #bec2ff; }

    /* Quiz feedback */
    .quiz-correct {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid #10B981 !important;
        border-radius: 6px;
        padding: 12px 16px;
        margin-top: 8px;
        color: #6EE7B7;
    }
    .quiz-incorrect {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid #EF4444 !important;
        border-radius: 6px;
        padding: 12px 16px;
        margin-top: 8px;
        color: #FCA5A5;
    }
</style>
""", unsafe_allow_html=True)

# Inject Global Stitch Theme
inject_theme()


# --- ACTIVITY LOGGING & MOCK DATA ---
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


# --- STATE MANAGEMENT & DEFAULTS ---
def init_state():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

    if "activity_log" not in st.session_state:
        st.session_state.activity_log = generate_mock_activity_log()

    # 1. Prerequisite Roadmap
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

    # 2. Sticky Notes
    if "sticky_notes" not in st.session_state:
        st.session_state.sticky_notes = [
            "IDS (Intrusion Detection System) operates out-of-band via TAP/SPAN port mirroring. It monitors and alerts on suspicious traffic without blocking packets inline.",
            "IPS (Intrusion Prevention System) sits directly inline with network traffic. It actively inspects packets in real-time and drops malicious flows before reaching hosts.",
            "Signature-Based vs Anomaly-Based: Both systems can use known attack signatures or statistical baseline heuristics to identify zero-day exploits.",
            "Key Architectural Difference: IDS failure maintains network availability (fail-open), whereas IPS inline failure could disrupt network connectivity (fail-closed)."
        ]

    # 3. Explain & Memorize Flashcards
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

    # 4. Quiz Builder
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = [
            {
                "question": "Where is an Intrusion Prevention System (IPS) deployed within a network topology?",
                "options": ["Out-of-band via SPAN/Mirror port", "Directly in-line with network traffic", "Exclusively on DNS root servers", "Inside end-user browser storage"],
                "answer": "Directly in-line with network traffic",
                "explanation": "An IPS must sit directly in the traffic pathway (in-line) to inspect, drop, or rewrite malicious packets before they reach destination hosts."
            },
            {
                "question": "What is the key functional difference between an IDS and an IPS?",
                "options": ["IDS detects and alerts; IPS detects and actively drops packets", "IDS operates only on Layer 2; IPS on Layer 7", "IDS encrypts traffic; IPS decrypts traffic", "There is no difference; they are synonymous"],
                "answer": "IDS detects and alerts; IPS detects and actively drops packets",
                "explanation": "IDS is a passive detection and telemetry alerting system, while IPS is active preventative enforcement."
            },
            {
                "question": "Which fail-state behavior is typical when an in-line IPS crashes without bypass hardware?",
                "options": ["Fail-Open (All traffic passes)", "Fail-Closed (Network traffic blocked)", "Automatic DNS sinkholing", "Instant conversion to IDS mode"],
                "answer": "Fail-Closed (Network traffic blocked)",
                "explanation": "Without specialized bypass NICs, an in-line device crash severs the physical/logical link, resulting in fail-closed downtime."
            },
            {
                "question": "How does Signature-Based Detection differ from Anomaly-Based Detection?",
                "options": ["Signatures match known byte patterns; Anomaly detects deviation from baseline statistical norms", "Signature detection requires AI; Anomaly uses static regex", "Signatures work only on encrypted packets", "Anomaly detection cannot identify zero-day vulnerabilities"],
                "answer": "Signatures match known byte patterns; Anomaly detects deviation from baseline statistical norms",
                "explanation": "Signature engines inspect known CVE strings/byte sequences, whereas anomaly engines detect unusual volumetric or behavioral spikes."
            },
            {
                "question": "Which network component is typically used to feed telemetry to a passive IDS?",
                "options": ["Network TAP or Switch SPAN/Mirror Port", "DHCP Option 82 Relay", "BGP Autonomous System Boundary Router", "RADIUS Accounting Agent"],
                "answer": "Network TAP or Switch SPAN/Mirror Port",
                "explanation": "TAPs and SPAN/mirror ports copy packets out-of-band to the IDS without impacting active forwarding latency."
            }
        ]
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

    # 5. Deep Dive Revision Notes
    if "revision_notes" not in st.session_state:
        st.session_state.revision_notes = """# Core Paradigm: Supervised vs. Unsupervised Learning

### Comprehensive Comparative Analysis

| Dimension | Supervised Learning | Unsupervised Learning |
| :--- | :--- | :--- |
| **Training Data** | Labeled Dataset: Pairs of inputs and target labels $\\{(x_i, y_i)\\}_{i=1}^N$ | Unlabeled Dataset: Input features only $\\{x_i\\}_{i=1}^N$ |
| **Objective Function** | Minimize empirical risk: $\\min_\\theta \\sum \\mathcal{L}(f_\\theta(x_i), y_i)$ | Uncover structural density, clusters, or latent manifold $p(x)$ |
| **Primary Tasks** | Classification, Regression, Object Detection | Clustering (K-Means, DBSCAN), Dimensionality Reduction (PCA, t-SNE) |
| **Evaluation Metrics** | Accuracy, Precision/Recall, $F_1$-score, MSE, $R^2$ | Silhouette Coefficient, Davies-Bouldin Index, Reconstruction Loss |
| **Human Supervision** | High (Costly ground-truth annotation pipeline required) | Zero human labeling required during dataset ingestion |

---

### Mathematical Foundations

#### 1. Supervised Empirical Loss Minimization
$$\\mathcal{L}_{MSE}(\\theta) = \\frac{1}{2N} \\sum_{i=1}^N \\left( y_i - \\mathbf{w}^T x_i - b \\right)^2$$

#### 2. Unsupervised Principal Component Analysis (PCA)
$$\\max_{\\mathbf{u}} \\mathbf{u}^T \\mathbf{\\Sigma} \\mathbf{u} \\quad \\text{s.t.} \\quad \\mathbf{u}^T \\mathbf{u} = 1$$
"""

init_state()

def switch_to_workspace():
    st.session_state.current_page = "workspace"

def switch_to_landing():
    st.session_state.current_page = "landing"

# --- AI SYNTHESIS PIPELINES ---
def run_explain_pipeline(topic_query):
    if not API_KEY:
        st.error("Gemini API key is not configured.")
        return False
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
You are an expert AI Educator.
Explain the topic: "{topic_query}".
Return a strictly valid JSON object with:
1. "explanation": A concise, clear explanation (2-3 paragraphs).
2. "flashcards": An array of exactly 5 Q&A objects ({{"q": "...", "a": "..."}}).

Output ONLY raw JSON.
"""
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
        prompt = f"""
Analyze the following study material and generate a 5-question multiple choice quiz:
\"\"\"{raw_content}\"\"\"

Output a strictly valid JSON array of 5 objects, each with:
- "question": string
- "options": array of exactly 4 strings
- "answer": string (exact match to one option)
- "explanation": string (why the answer is correct)

Output ONLY raw JSON.
"""
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
        prompt = """
You are the Study OS Multimodal AI Engine.
Analyze the user's input context and generate a complete, structured JSON payload.

Your JSON output MUST follow this exact schema:
{
  "mermaid": "graph TD\\n  A[...] --> B[...]\\n  ...",
  "sticky_notes": [
    "Short key fact 1 (max 2 sentences)",
    "Short key fact 2 (max 2 sentences)",
    "Short key fact 3 (max 2 sentences)",
    "Short key fact 4 (max 2 sentences)"
  ],
  "revision_notes": "# Markdown Study Guide\\n\\n### Key Concepts\\n... (include tables, LaTeX formulas, code blocks)"
}

Output raw JSON only.
"""
        contents = [prompt]
        if context_text and context_text.strip():
            contents.append(f"Context Text / Syllabus / Lecture Notes:\n{context_text.strip()}")
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


# --- ROUTING LOGIC ---

if st.session_state.current_page == "landing":
    # ==========================================
    # PAGE 1: STITCH EXECUTIVE LANDING PAGE
    # ==========================================
    
    # Top Bar Header
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #232426; padding-bottom: 14px; margin-bottom: 36px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 32px; height: 32px; background: #191A1C; border: 1px solid #232426; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-family: 'Manrope'; color: #bec2ff; font-size: 14px;">S</div>
                <div>
                    <div style="font-family: 'Manrope'; font-weight: 700; font-size: 1.1rem; letter-spacing: -0.04em; color: #FFFFFF;">STUDY OS</div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.65rem; color: #9A9DA3; letter-spacing: 0.1em; text-transform: uppercase;">Precision Learning Platform</div>
                </div>
            </div>
            <div style="display: flex; gap: 20px; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #9A9DA3; align-items: center;">
                <span style="color: #50d8e9; border: 1px solid rgba(80,216,233,0.3); padding: 2px 8px; border-radius: 3px; background: rgba(80,216,233,0.05);">TELEMETRY: ACTIVE</span>
                <span>LATENCY: 12ms</span>
                <span>STATUS: NOMINAL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div style="text-align: center; margin-top: 3rem; margin-bottom: 3.5rem;">
            <div class="mono-telemetry" style="margin-bottom: 1.25rem; color: #50d8e9 !important;">// MULTIMODAL KNOWLEDGE SYNTHESIS</div>
            <h1 class="hero-headline">Ingest the lecture.<br>Map the memory.</h1>
            <p style="color: #9A9DA3; max-width: 680px; margin: 0 auto 2.5rem auto; font-size: 1.1rem; line-height: 1.6; font-family: 'Inter';">
                An institutional intelligence engine engineered for rapid lecture distillation, active-recall memory generation, interactive topological dependency roadmaps, and spaced repetition analytics.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.button("INITIALIZE WORKSPACE", on_click=switch_to_workspace, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='mono-telemetry' style='text-align: center; margin-bottom: 1.5rem;'>Executive Architecture</div>", unsafe_allow_html=True)

    bento1, bento2, bento3 = st.columns(3, gap="medium")

    with bento1:
        st.markdown("""
            <div class="stitch-glass-panel">
                <span style="position: absolute; top: 12px; left: 16px; font-family: 'JetBrains Mono'; font-size: 10px; color: #9A9DA3;">FIG. 1 // INGESTION</span>
                <div style="margin-top: 24px;">
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">🎙️ Multimodal Vector Intake</h3>
                    <p style="color: #9A9DA3; font-size: 0.9rem; line-height: 1.55;">Stream audio dictation, whiteboard scans, and raw curriculum text through high-throughput Gemini multimodal pipelines.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with bento2:
        st.markdown("""
            <div class="stitch-glass-panel">
                <span style="position: absolute; top: 12px; left: 16px; font-family: 'JetBrains Mono'; font-size: 10px; color: #9A9DA3;">FIG. 2 // EVALUATION</span>
                <div style="margin-top: 24px;">
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">⚡ Generative Exam Suites</h3>
                    <p style="color: #9A9DA3; font-size: 0.9rem; line-height: 1.55;">Autonomously synthesize study materials into interactive multiple-choice test suites and active recall memory banks.</p>
                    <div style="background: #151618; padding: 10px 12px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem; border: 1px solid #232426; color: #bec2ff; margin-top: 12px;"><b>Module:</b> IDS vs IPS Automated Exam Suite</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with bento3:
        st.markdown("""
            <div class="stitch-glass-panel">
                <span style="position: absolute; top: 12px; left: 16px; font-family: 'JetBrains Mono'; font-size: 10px; color: #9A9DA3;">FIG. 3 // TELEMETRY</span>
                <div style="margin-top: 24px;">
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">📊 Spaced Repetition Matrix</h3>
                    <p style="color: #9A9DA3; font-size: 0.9rem; line-height: 1.55;">Track active retention curves, consistency velocity, and memory stability on an authentic high-density activity grid.</p>
                    <div style="background: #151618; padding: 10px 12px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem; border: 1px solid #232426; color: #50d8e9; margin-top: 12px;"><b>Telemetry:</b> 45-Day Retention Vector</div>
                </div>
            </div>
        """, unsafe_allow_html=True)


elif st.session_state.current_page == "workspace":
    # ==========================================
    # PAGE 2: STITCH STUDY OS WORKSPACE DASHBOARD
    # ==========================================

    # Stitch Top App Bar
    st.markdown("""
        <header style="background: rgba(19, 19, 20, 0.95); backdrop-filter: blur(20px); border-bottom: 1px solid #232426; display: flex; justify-content: space-between; align-items: center; height: 56px; padding: 0 16px; margin-bottom: 24px; border-radius: 6px;">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="width: 26px; height: 26px; background: #5E6BFF; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-family: 'Manrope'; color: #fff; font-size: 13px;">S</div>
                <span style="font-family: 'Manrope'; font-weight: 700; font-size: 1rem; letter-spacing: -0.04em; color: #FFFFFF;">STUDY OS</span>
                <div style="display: flex; gap: 16px; margin-left: 20px; font-family: 'JetBrains Mono'; font-size: 0.75rem;">
                    <span style="color: #bec2ff; border-bottom: 2px solid #5E6BFF; padding-bottom: 4px;">WORKSPACE</span>
                    <span style="color: #9A9DA3;">TELEMETRY</span>
                    <span style="color: #9A9DA3;">PERFORMANCE</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <span class="mono-telemetry" style="color: #50d8e9;">SYSTEM: OPTIMAL</span>
            </div>
        </header>
    """, unsafe_allow_html=True)

    # Disconnect / Navigation Control
    nav_col1, nav_col2 = st.columns([4, 1])
    with nav_col2:
        st.button("← Disconnect", on_click=switch_to_landing, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Master Multimodal Input Stream
    with st.container(border=True):
        st.markdown("### ⚡ Master Ingestion Stream")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.25rem;'>Provide lecture context via transcript, audio, or whiteboard scan to recompile all Study OS modules simultaneously.</p>", unsafe_allow_html=True)

        with st.form("master_input_form"):
            form_col1, form_col2 = st.columns([2, 1], gap="medium")
            with form_col1:
                input_text = st.text_area(
                    "Lecture Transcript / Syllabus Notes / Manual Prompt",
                    placeholder="Enter lecture transcript, syllabus outline, or technical topics here...",
                    height=130
                )
            with form_col2:
                input_audio = st.audio_input("Voice Dictation")
                input_camera = st.camera_input("Whiteboard Scan")

            submit_btn = st.form_submit_button("PROCESS & RESTRUCTURE STUDY OS", use_container_width=True)

        if submit_btn:
            if not (input_text or input_audio or input_camera):
                st.warning("Please provide at least one input stream (text, audio, or whiteboard scan).")
            else:
                with st.spinner("Analyzing lecture semantics and compiling Study OS data structures..."):
                    success = run_study_os_pipeline(input_text, input_audio, input_camera)
                    if success:
                        st.success("Study OS modules updated successfully!")
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabbed Navigation Architecture matching Stitch Modules
    tab_explain, tab_quiz, tab_analytics, tab_sticky, tab_roadmap, tab_deepdive = st.tabs([
        "💡 Explain & Memorize",
        "📝 Quiz Builder",
        "📊 Analytics & Roadmap",
        "📌 Sticky Notes",
        "🗺️ Prerequisite Graph",
        "📖 Deep Dive"
    ])

    # ----------------------------------------------------
    # TAB 1: EXPLAIN & MEMORIZE (Stitch Screen 1d1c6f28012d4965be52f1fb761ff19b)
    # ----------------------------------------------------
    with tab_explain:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>Autonomous Concept Synthesis</div>", unsafe_allow_html=True)
        st.markdown("### Explain & Memorize")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Synthesize clear explanations and active-recall flashcard sets from any single topic prompt.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.form("explain_form"):
                topic_input = st.text_input("Enter Topic to Explain", value=st.session_state.explain_topic, placeholder="e.g. Principal Component Analysis, Dynamic Programming...")
                explain_submit = st.form_submit_button("SYNTHESIZE EXPLANATION & FLASHCARDS")
            
            if explain_submit and topic_input:
                with st.spinner("Synthesizing concept and building memory cards..."):
                    if run_explain_pipeline(topic_input):
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Explanation in Stitch Card
        with st.container(border=True):
            st.markdown(f"#### 📖 Synthesis Breakdown: *{st.session_state.explain_topic}*")
            st.markdown(f"<p style='color: #e5e2e3; font-size: 0.98rem; line-height: 1.7;'>{st.session_state.explanation_text}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🗃️ Active-Recall Memory Vector Cards")

        for idx, card in enumerate(st.session_state.explain_flashcards):
            with st.container(border=True):
                st.markdown(f"**Q{idx+1}: {card['q']}**")
                with st.expander("👁️ Reveal Answer"):
                    st.markdown(f"<span style='color: #50d8e9; font-weight: 500;'>{card['a']}</span>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 2: QUIZ BUILDER (Stitch Screen 3e586838e9564c7c882d445bba7c781b)
    # ----------------------------------------------------
    with tab_quiz:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>Evaluative Assessment Engine</div>", unsafe_allow_html=True)
        st.markdown("### The Quiz Builder")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Synthesize an interactive 5-question multiple choice assessment from raw curriculum text.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.form("quiz_gen_form"):
                raw_text_input = st.text_area("Paste Content for Quiz Generation", placeholder="Paste lecture notes, articles, or transcripts...", height=110)
                gen_quiz_btn = st.form_submit_button("GENERATE 5-QUESTION QUIZ")

            if gen_quiz_btn and raw_text_input:
                with st.spinner("Analyzing text and constructing evaluation questions..."):
                    if run_quiz_builder_pipeline(raw_text_input):
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive Quiz Evaluation
        with st.form("quiz_eval_form"):
            user_answers = {}
            for q_idx, q_item in enumerate(st.session_state.quiz_data):
                st.markdown(f"##### Question {q_idx+1}: {q_item['question']}")
                user_answers[q_idx] = st.radio(
                    f"Options for Q{q_idx+1}",
                    options=q_item["options"],
                    key=f"quiz_opt_{q_idx}",
                    label_visibility="collapsed"
                )
                st.markdown("<hr style='border-color: #232426; margin: 15px 0;'>", unsafe_allow_html=True)
            
            submit_quiz = st.form_submit_button("SUBMIT QUIZ FOR EVALUATION")

        if submit_quiz:
            st.session_state.quiz_submitted = True
            correct_count = 0
            for q_idx, q_item in enumerate(st.session_state.quiz_data):
                if user_answers[q_idx] == q_item["answer"]:
                    correct_count += 1
            st.session_state.quiz_score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            log_activity("Quiz", topic="Quiz Submission", mastery_score=st.session_state.quiz_score)

        if st.session_state.get("quiz_submitted", False):
            st.markdown("<br>", unsafe_allow_html=True)
            score_col1, score_col2 = st.columns([1, 3])
            with score_col1:
                st.metric("Quiz Score", f"{st.session_state.quiz_score}%", delta=f"{st.session_state.quiz_score - 70}% vs Threshold")
            
            st.markdown("#### 🎯 Detailed Answer Key & Explanations")
            for q_idx, q_item in enumerate(st.session_state.quiz_data):
                user_ans = user_answers.get(q_idx, "")
                is_correct = (user_ans == q_item["answer"])
                
                if is_correct:
                    st.markdown(f"""
                    <div class="quiz-correct">
                        <b>Q{q_idx+1}: Correct!</b><br>
                        Your Answer: {user_ans}<br>
                        <i>{q_item['explanation']}</i>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="quiz-incorrect">
                        <b>Q{q_idx+1}: Incorrect</b><br>
                        Your Answer: {user_ans} | <b>Correct Answer:</b> {q_item['answer']}<br>
                        <i>{q_item['explanation']}</i>
                    </div>
                    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 3: ANALYTICS & ROADMAP (Stitch Screen 8cc791d966774bf599cc103185559bb2)
    # ----------------------------------------------------
    with tab_analytics:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>System Analytics // Telemetry & Habits</div>", unsafe_allow_html=True)
        st.markdown("### System Analytics & Roadmap")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Runtime telemetry, retention velocity, and prerequisite topology.</p>", unsafe_allow_html=True)

        df_act = st.session_state.activity_log
        total_activities = len(df_act)
        avg_retention = int(df_act["Mastery_Score"].mean()) if not df_act.empty else 94
        unique_days = df_act["Date"].nunique() if not df_act.empty else 42

        # 3 KPI Cards matching FIG. 1, FIG. 2, FIG. 3 from Stitch Screen
        kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
        with kpi1:
            st.metric("Cards Mastered", f"{total_activities * 28:,}", delta="+12% vs last week")
        with kpi2:
            st.metric("Current Streak", f"{unique_days} Days", delta="Optimal consistency")
        with kpi3:
            st.metric("Retention Rate", f"{avg_retention}.2%", delta="Target: 95%")

        st.markdown("<br>", unsafe_allow_html=True)

        # FIG. 4 // Activity Signal (52-week Heatmap Grid from Stitch Screen)
        with st.container(border=True):
            st.markdown("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                    <span class="mono-telemetry">FIG. 4 // ACTIVITY SIGNAL</span>
                    <span style="font-family: 'JetBrains Mono'; font-size: 10px; color: #9A9DA3;">LAST 365 DAYS</span>
                </div>
            """, unsafe_allow_html=True)
            
            daily_counts = df_act.groupby("Date").size().to_dict()
            today = datetime.now().date()
            start_date = today - timedelta(days=83)
            
            heatmap_html = """
            <div style="background-color: #070708; padding: 20px; border-radius: 4px; border: 1px solid #232426; overflow-x: auto;">
                <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: 6px;">
            """
            for week in range(12):
                heatmap_html += "<div style='display: flex; flex-direction: column; gap: 6px;'>"
                for day in range(7):
                    cell_date = start_date + timedelta(days=week*7 + day)
                    date_str = cell_date.strftime("%Y-%m-%d")
                    count = daily_counts.get(date_str, 0)
                    
                    if count == 0:
                        level_class = ""
                    elif count == 1:
                        level_class = "level-1"
                    elif count == 2:
                        level_class = "level-2"
                    elif count == 3:
                        level_class = "level-3"
                    else:
                        level_class = "level-4"
                    
                    heatmap_html += f'<div class="heatmap-cell {level_class}" title="{date_str}: {count} sessions logged"></div>'
                heatmap_html += "</div>"
            
            heatmap_html += """
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #9A9DA3;">
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

        st.markdown("<br>", unsafe_allow_html=True)

        # FIG. 5 // Knowledge Topology (Roadmap from Stitch Screen)
        with st.container(border=True):
            st.markdown("<span class='mono-telemetry'>FIG. 5 // KNOWLEDGE TOPOLOGY ROADMAP</span>", unsafe_allow_html=True)
            mermaid_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
                <style>
                    body {{
                        margin: 0;
                        padding: 16px;
                        background: transparent;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-family: 'Inter', sans-serif;
                    }}
                    .mermaid {{
                        width: 100%;
                        display: flex;
                        justify-content: center;
                    }}
                </style>
            </head>
            <body>
                <div class="mermaid">
                    {st.session_state.mermaid_code}
                </div>
                <script>
                    mermaid.initialize({{
                        startOnLoad: true,
                        theme: 'dark',
                        themeVariables: {{
                            darkMode: true,
                            background: '#070708',
                            primaryColor: '#101112',
                            primaryTextColor: '#e5e2e3',
                            primaryBorderColor: '#5E6BFF',
                            lineColor: '#bec2ff',
                            secondaryColor: '#191A1C',
                            tertiaryColor: '#070708'
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            components.html(mermaid_html, height=440, scrolling=True)

    # ----------------------------------------------------
    # TAB 4: DIGITAL STICKY NOTES
    # ----------------------------------------------------
    with tab_sticky:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>Active Recall Matrix</div>", unsafe_allow_html=True)
        st.markdown("### Digital Corkboard")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Key lecture insights and critical conceptual distinctions.</p>", unsafe_allow_html=True)

        cols = st.columns(4, gap="medium")
        for i, note in enumerate(st.session_state.sticky_notes):
            col = cols[i % 4]
            with col:
                note_html = f"""
                <div class="stitch-note-card">
                    <div class="stitch-note-num">NOTE #{i+1:02d}</div>
                    <div class="stitch-note-body">{note}</div>
                </div>
                """
                st.markdown(note_html, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 5: PREREQUISITE GRAPH
    # ----------------------------------------------------
    with tab_roadmap:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>Dynamic Knowledge Graph</div>", unsafe_allow_html=True)
        st.markdown("### Prerequisite Dependency Tree")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Concept tree mapping foundational topics to advanced engineering targets.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            components.html(mermaid_html, height=480, scrolling=True)

    # ----------------------------------------------------
    # TAB 6: IN-DEPTH REVISION NOTES (Markdown & LaTeX)
    # ----------------------------------------------------
    with tab_deepdive:
        st.markdown("<div class='mono-telemetry' style='margin-bottom: 0.5rem;'>Comprehensive Study Guide</div>", unsafe_allow_html=True)
        st.markdown("### In-Depth Revision & Formal Notes")
        st.markdown("<p style='color: #9A9DA3; font-size: 0.92rem; margin-bottom: 1.5rem;'>Rigorous notes, mathematical derivations, comparison matrices, and code references.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.expander("📚 Expand Full Revision Module", expanded=True):
                st.markdown(st.session_state.revision_notes)
