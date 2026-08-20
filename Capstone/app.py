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
    page_title="Classroom Memory: Study OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# --- CSS OVERRIDES & STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Nuke Streamlit default headers & footers */
    #MainMenu, header, footer {visibility: hidden !important;}
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 3.5rem !important;
        padding-right: 3.5rem !important;
        max-width: 1400px !important;
    }

    /* Base theme - dark HUD aesthetic with blueprint grid */
    .stApp {
        background-color: #0d0f12 !important;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
        background-size: 24px 24px;
        font-family: 'Inter', sans-serif !important;
        color: #E2E8F0 !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        color: #FFFFFF !important;
    }

    .hero-title {
        font-size: 4.5rem !important;
        line-height: 1.05 !important;
        font-weight: 900 !important;
        background: linear-gradient(180deg, #FFFFFF 20%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.25rem !important;
    }

    .micro-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: #60A5FA !important;
    }

    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        background-color: rgba(17, 20, 24, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 20px !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        transition: transform 0.3s ease, border-color 0.3s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(255, 255, 255, 0.16) !important;
    }

    /* Tab navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: rgba(15, 18, 22, 0.7);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #94A3B8 !important;
        border-radius: 8px !important;
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
        background: rgba(255, 255, 255, 0.1) !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
    }

    /* Buttons */
    .stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        padding: 10px 22px !important;
        border-radius: 8px !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
    }

    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(180deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: 1px solid #3B82F6 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.35) !important;
    }

    [data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(180deg, #3B82F6 0%, #2563EB 100%) !important;
        border-color: #60A5FA !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.5) !important;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: rgba(22, 26, 32, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        color: #94A3B8 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }

    /* Digital Sticky Note styling (#FDE68A palette) */
    .sticky-note-card {
        background-color: #FDE68A !important;
        color: #1F2937 !important;
        border-radius: 6px !important;
        padding: 20px !important;
        min-height: 200px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.4) !important;
        position: relative !important;
        margin-bottom: 20px !important;
        font-family: 'Inter', sans-serif !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
        border-left: 4px solid #F59E0B !important;
    }

    .sticky-note-card:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.7) !important;
    }

    .sticky-tape {
        position: absolute;
        top: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 18px;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 1px 3px rgba(0,0,0,0.15);
    }

    .sticky-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 700;
        color: #B45309;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .sticky-body {
        font-size: 0.92rem;
        line-height: 1.5;
        font-weight: 500;
        color: #1E293B;
    }

    /* Flip-card & Explanation cards */
    .flashcard-item {
        background: rgba(26, 31, 38, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        transition: all 0.25s ease;
    }
    .flashcard-item:hover {
        border-color: #3B82F6;
        transform: translateX(4px);
    }

    /* Quiz feedback */
    .quiz-correct {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        color: #6EE7B7;
    }
    .quiz-incorrect {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid #EF4444 !important;
        border-radius: 8px;
        padding: 12px 16px;
        margin-top: 10px;
        color: #FCA5A5;
    }
</style>
""", unsafe_allow_html=True)


# --- ACTIVITY LOGGING & MOCK DATA ---
def generate_mock_activity_log():
    activities = ["Flashcard", "Quiz", "Roadmap", "Deep Dive"]
    topics = ["Data Science", "Web Security", "Competitive Programming"]
    rows = []
    base_date = datetime.now().date()
    
    np.random.seed(42)
    for i in range(45, 0, -1):
        d = base_date - timedelta(days=i)
        # Random number of activities for this day
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

    classDef default fill:#1e232a,stroke:#3b82f6,stroke-width:1.5px,color:#f8fafc;
    classDef startNode fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#ffffff;
    classDef targetNode fill:#065f46,stroke:#34d399,stroke-width:2px,color:#ffffff;
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
        model = genai.GenerativeModel("gemini-1.5-pro")
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
        model = genai.GenerativeModel("gemini-1.5-pro")
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
        model = genai.GenerativeModel("gemini-1.5-pro")
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
    # PAGE 1: THE LANDING PAGE
    # ==========================================
    
    st.markdown("""
        <div style="text-align: center; margin-top: 5rem; margin-bottom: 3.5rem;">
            <div class="micro-label" style="margin-bottom: 1.25rem;">// CLASSROOM MEMORY: STUDY OS v2.5</div>
            <h1 class="hero-title">Ingest the lecture.<br>Map the memory.</h1>
            <p style="color: #94A3B8; max-width: 680px; margin: 0 auto 2.5rem auto; font-size: 1.15rem; line-height: 1.6;">
                The multimodal intelligence engine for rapid knowledge deconstruction, interactive roadmaps, digital sticky notes, AI quiz synthesis, and spaced repetition analytics.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.button("INITIALIZE WORKSPACE", on_click=switch_to_workspace, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='micro-label' style='text-align: center; margin-bottom: 1.5rem;'>Engine Capabilities</div>", unsafe_allow_html=True)

    bento1, bento2, bento3 = st.columns(3, gap="large")

    with bento1:
        with st.container(border=True):
            st.markdown("### 🎙️ Multimodal Intake")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Ingest audio dictation, whiteboard scans, and raw curriculum text with Gemini vision and audio pipelines.</p>", unsafe_allow_html=True)

    with bento2:
        with st.container(border=True):
            st.markdown("### ⚡ Generative Quizzes & Flashcards")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Autonomously distill topics into interactive multiple-choice test suites and flip-card memory banks.</p>", unsafe_allow_html=True)
            st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 12px 14px; border-radius: 8px; font-family: JetBrains Mono, monospace; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.06); color: #CBD5E1;'><b>Module:</b> IDS vs IPS Automated Exam Suite</div>", unsafe_allow_html=True)

    with bento3:
        with st.container(border=True):
            st.markdown("### 📊 Spaced Repetition Mastery")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Track active retention curves and consistency with an authentic GitHub-style activity matrix.</p>", unsafe_allow_html=True)
            st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 12px 14px; border-radius: 8px; font-family: JetBrains Mono, monospace; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.06); color: #CBD5E1;'><b>Telemetry:</b> 45-Day Retention Vector</div>", unsafe_allow_html=True)


elif st.session_state.current_page == "workspace":
    # ==========================================
    # PAGE 2: STUDY OS DASHBOARD
    # ==========================================

    # Navigation Breadcrumb Bar
    nav_left, nav_right = st.columns([3, 1])
    with nav_left:
        st.markdown("<div class='micro-label' style='padding-top: 10px;'><span style='color: #60A5FA;'>// SYSTEM</span> / STUDY OS DASHBOARD</div>", unsafe_allow_html=True)
    with nav_right:
        st.button("← Back to Landing", on_click=switch_to_landing, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Master Multimodal Input Stream
    with st.container(border=True):
        st.markdown("### ⚡ Master Ingestion Stream")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.25rem;'>Provide lecture context via text, voice, or camera scan to update all OS modules simultaneously.</p>", unsafe_allow_html=True)

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

    # Tabbed Navigation Architecture
    tab_roadmap, tab_sticky, tab_explain, tab_quiz, tab_deepdive, tab_analytics = st.tabs([
        "🗺️ Roadmap",
        "📌 Sticky Notes",
        "💡 Explain & Memorize",
        "📝 Quiz Builder",
        "📖 Deep Dive",
        "📊 Mastery Graph"
    ])

    # ----------------------------------------------------
    # TAB 1: THE PREREQUISITE ROADMAP (Mermaid.js)
    # ----------------------------------------------------
    with tab_roadmap:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Dynamic Knowledge Graph</div>", unsafe_allow_html=True)
        st.markdown("### Prerequisite Dependency Roadmap")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Interactive dependency tree visualizing concepts and logical progression.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            mermaid_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
                <style>
                    body {{
                        margin: 0;
                        padding: 20px;
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
                            background: '#0d0f12',
                            primaryColor: '#1e293b',
                            primaryTextColor: '#f8fafc',
                            primaryBorderColor: '#3b82f6',
                            lineColor: '#60a5fa',
                            secondaryColor: '#334155',
                            tertiaryColor: '#0f172a'
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            components.html(mermaid_html, height=480, scrolling=True)

    # ----------------------------------------------------
    # TAB 2: DIGITAL STICKY NOTES (CSS Grid in st.columns)
    # ----------------------------------------------------
    with tab_sticky:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Active Recall Matrix</div>", unsafe_allow_html=True)
        st.markdown("### Digital Corkboard")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Key lecture insights and critical conceptual distinctions.</p>", unsafe_allow_html=True)

        cols = st.columns(4, gap="medium")
        for i, note in enumerate(st.session_state.sticky_notes):
            col = cols[i % 4]
            with col:
                note_html = f"""
                <div class="sticky-note-card">
                    <div class="sticky-tape"></div>
                    <div class="sticky-num">NOTE #{i+1:02d}</div>
                    <div class="sticky-body">{note}</div>
                </div>
                """
                st.markdown(note_html, unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 3: EXPLAIN & MEMORIZE (Issue #4)
    # ----------------------------------------------------
    with tab_explain:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Autonomous Concept Synthesis</div>", unsafe_allow_html=True)
        st.markdown("### Explain & Memorize")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Synthesize clear explanations and active-recall flashcard sets from any single topic prompt.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.form("explain_form"):
                topic_input = st.text_input("Enter Topic to Explain", value=st.session_state.explain_topic, placeholder="e.g. Principal Component Analysis, Dynamic Programming...")
                explain_submit = st.form_submit_button("SYNTHESIZE EXPLANATION & FLASHCARDS")
            
            if explain_submit and topic_input:
                with st.spinner("Synthesizing concept and building memory cards..."):
                    if run_explain_pipeline(topic_input):
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Explanation
        with st.container(border=True):
            st.markdown(f"#### 📖 Comprehensive Explanation: *{st.session_state.explain_topic}*")
            st.markdown(f"<p style='color: #CBD5E1; font-size: 1rem; line-height: 1.7;'>{st.session_state.explanation_text}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🗃️ Active-Recall Memory Cards")

        for idx, card in enumerate(st.session_state.explain_flashcards):
            with st.container(border=True):
                st.markdown(f"**Q{idx+1}: {card['q']}**")
                with st.expander("👁️ Reveal Answer"):
                    st.markdown(f"<span style='color: #60A5FA;'>{card['a']}</span>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # TAB 4: QUIZ BUILDER (Issue #4)
    # ----------------------------------------------------
    with tab_quiz:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Evaluative Assessment Engine</div>", unsafe_allow_html=True)
        st.markdown("### The Quiz Builder")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Synthesize an interactive 5-question multiple choice assessment from raw curriculum text.</p>", unsafe_allow_html=True)

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
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 15px 0;'>", unsafe_allow_html=True)
            
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
    # TAB 5: IN-DEPTH REVISION NOTES (Markdown & LaTeX)
    # ----------------------------------------------------
    with tab_deepdive:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Comprehensive Study Guide</div>", unsafe_allow_html=True)
        st.markdown("### In-Depth Revision & Formal Notes")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Rigorous notes, mathematical derivations, comparison matrices, and code references.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.expander("📚 Expand Full Revision Module", expanded=True):
                st.markdown(st.session_state.revision_notes)

    # ----------------------------------------------------
    # TAB 6: MASTERY GRAPH & ANALYTICS (Issue #6)
    # ----------------------------------------------------
    with tab_analytics:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Telemetry & Study Habits</div>", unsafe_allow_html=True)
        st.markdown("### Mastery Graph & Spaced Repetition Analytics")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Temporal tracking of active study sessions, retention metrics, and mastery velocity.</p>", unsafe_allow_html=True)

        # 3 KPI Cards
        df_act = st.session_state.activity_log
        total_activities = len(df_act)
        avg_retention = int(df_act["Mastery_Score"].mean()) if not df_act.empty else 85
        unique_days = df_act["Date"].nunique() if not df_act.empty else 12

        kpi1, kpi2, kpi3 = st.columns(3, gap="medium")
        with kpi1:
            st.metric("Current Streak", f"{unique_days} Days", delta="+3 Days this week")
        with kpi2:
            st.metric("Cards Mastered", f"{total_activities * 4}", delta="+28 Mastered")
        with kpi3:
            st.metric("System Retention Rate", f"{avg_retention}%", delta="+4.2% Optimal")

        st.markdown("<br>", unsafe_allow_html=True)

        # GitHub-Style Heatmap Grid
        with st.container(border=True):
            st.markdown("#### 🔥 90-Day Contribution & Study Matrix")
            
            # Aggregate counts per day
            daily_counts = df_act.groupby("Date").size().to_dict()
            
            # Generate past 12 weeks of calendar grid (12 cols x 7 rows)
            today = datetime.now().date()
            start_date = today - timedelta(days=83)
            
            # Build CSS Heatmap
            heatmap_html = """
            <div style="background-color: #161616; padding: 24px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); overflow-x: auto;">
                <div style="display: grid; grid-template-columns: repeat(12, 1fr); gap: 8px;">
            """
            
            for week in range(12):
                heatmap_html += "<div style='display: flex; flex-direction: column; gap: 8px;'>"
                for day in range(7):
                    cell_date = start_date + timedelta(days=week*7 + day)
                    date_str = cell_date.strftime("%Y-%m-%d")
                    count = daily_counts.get(date_str, 0)
                    
                    # Color scale from #161616 (empty) to #9A3923 -> #F2613F (active)
                    if count == 0:
                        bg_color = "rgba(255, 255, 255, 0.05)"
                    elif count == 1:
                        bg_color = "#5c2415"
                    elif count == 2:
                        bg_color = "#9A3923"
                    elif count == 3:
                        bg_color = "#c74728"
                    else:
                        bg_color = "#F2613F"
                    
                    heatmap_html += f"""
                    <div title="{date_str}: {count} activities logged" 
                         style="width: 100%; aspect-ratio: 1; border-radius: 4px; background-color: {bg_color}; transition: transform 0.2s;"
                         onmouseover="this.style.transform='scale(1.2)';" 
                         onmouseout="this.style.transform='scale(1)';" >
                    </div>
                    """
                heatmap_html += "</div>"
            
            heatmap_html += """
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 16px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">
                    <span>Less</span>
                    <span style="width: 12px; height: 12px; background-color: rgba(255,255,255,0.05); border-radius: 2px;"></span>
                    <span style="width: 12px; height: 12px; background-color: #5c2415; border-radius: 2px;"></span>
                    <span style="width: 12px; height: 12px; background-color: #9A3923; border-radius: 2px;"></span>
                    <span style="width: 12px; height: 12px; background-color: #c74728; border-radius: 2px;"></span>
                    <span style="width: 12px; height: 12px; background-color: #F2613F; border-radius: 2px;"></span>
                    <span>More</span>
                </div>
            </div>
            """
            st.markdown(heatmap_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📋 Raw Telemetry Activity Log")
            st.dataframe(df_act.sort_values(by="Date", ascending=False), use_container_width=True, height=240)
