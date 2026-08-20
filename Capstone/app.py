import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
import os
import json
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

    /* Base theme - high editorial dark mode with blueprint grid */
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

    /* Container Glassmorphism */
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
        gap: 8px;
        background-color: rgba(15, 18, 22, 0.6);
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #94A3B8 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
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

    /* Expanders styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT & DEFAULTS ---
def init_state():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"

    # 1. Default Prerequisite Roadmap (Theory of Computation -> Software Engineering Testing Models)
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

    # 2. Default Sticky Notes (Web Security: IDS vs IPS)
    if "sticky_notes" not in st.session_state:
        st.session_state.sticky_notes = [
            "IDS (Intrusion Detection System) operates out-of-band via TAP/SPAN port mirroring. It monitors and alerts on suspicious traffic without blocking packets inline.",
            "IPS (Intrusion Prevention System) sits directly inline with network traffic. It actively inspects packets in real-time and drops malicious flows before reaching hosts.",
            "Signature-Based vs Anomaly-Based: Both systems can use known attack signatures or statistical baseline heuristics to identify zero-day exploits.",
            "Key Architectural Difference: IDS failure maintains network availability (fail-open), whereas IPS inline failure could disrupt network connectivity (fail-closed)."
        ]

    # 3. Default In-Depth Revision Notes (Supervised vs. Unsupervised Learning)
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
In standard linear/logistic regression and neural networks:
$$\\mathcal{L}_{MSE}(\\theta) = \\frac{1}{2N} \\sum_{i=1}^N \\left( y_i - \\mathbf{w}^T x_i - b \\right)^2$$

#### 2. Unsupervised Principal Component Analysis (PCA)
Maximizing projection variance onto orthogonal eigenvectors of covariance matrix $\\mathbf{\\Sigma}$:
$$\\max_{\\mathbf{u}} \\mathbf{u}^T \\mathbf{\\Sigma} \\mathbf{u} \\quad \\text{s.t.} \\quad \\mathbf{u}^T \\mathbf{u} = 1$$

```python
# Quick Implementation Reference
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# Supervised Classifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Unsupervised Dimensionality Reduction
pca = PCA(n_components=2)
X_latent = pca.fit_transform(X_raw)
```
"""

init_state()

def switch_to_workspace():
    st.session_state.current_page = "workspace"

def switch_to_landing():
    st.session_state.current_page = "landing"

# --- GEMINI STRUCTURED PAYLOAD INGESTION ---
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

Requirements:
1. mermaid: A valid Mermaid.js flowchart (graph TD or graph LR) mapping prerequisites, architectural flows, or topic hierarchies. Ensure node text uses brackets like A[Title].
2. sticky_notes: An array of exactly 4 concise, high-impact key takeaways.
3. revision_notes: Detailed revision notes with markdown comparison tables, headers, and LaTeX equations if applicable.
4. Output raw JSON only.
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

        # Clean JSON code blocks
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        payload = json.loads(raw_text.strip())

        if "mermaid" in payload and payload["mermaid"]:
            st.session_state.mermaid_code = payload["mermaid"].strip()
        if "sticky_notes" in payload and isinstance(payload["sticky_notes"], list) and len(payload["sticky_notes"]) >= 4:
            st.session_state.sticky_notes = payload["sticky_notes"][:4]
        if "revision_notes" in payload and payload["revision_notes"]:
            st.session_state.revision_notes = payload["revision_notes"]

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
            <div class="micro-label" style="margin-bottom: 1.25rem;">// CLASSROOM MEMORY: STUDY OS v2.0</div>
            <h1 class="hero-title">Ingest the lecture.<br>Map the memory.</h1>
            <p style="color: #94A3B8; max-width: 680px; margin: 0 auto 2.5rem auto; font-size: 1.15rem; line-height: 1.6;">
                The multimodal intelligence engine for rapid knowledge deconstruction, interactive roadmaps, digital sticky notes, and deep technical revision.
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
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Ingest audio dictation, whiteboard scans, and raw curriculum text. Processed with Gemini multimodal context handling.</p>", unsafe_allow_html=True)

    with bento2:
        with st.container(border=True):
            st.markdown("### ⚡ Auto-Deconstruction")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Distill complex lecture discussions into high-impact digital sticky notes and structured comparisons.</p>", unsafe_allow_html=True)
            st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 12px 14px; border-radius: 8px; font-family: JetBrains Mono, monospace; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.06); color: #CBD5E1;'><b>Input:</b> Audio on Web Security<br><b>Output:</b> Distinguishing IDS vs IPS Architectures</div>", unsafe_allow_html=True)

    with bento3:
        with st.container(border=True):
            st.markdown("### 🗺️ Prerequisite Mapping")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.6;'>Dynamic Mermaid.js flowchart rendering to visually connect foundational concepts to target domains.</p>", unsafe_allow_html=True)
            st.markdown("<div style='background: rgba(255,255,255,0.03); padding: 12px 14px; border-radius: 8px; font-family: JetBrains Mono, monospace; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.06); color: #CBD5E1;'><b>Map:</b> Theory of Computation &rarr; Software Engineering Testing Models</div>", unsafe_allow_html=True)


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

    # Master Input Form
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
    tab_roadmap, tab_sticky, tab_deepdive = st.tabs(["🗺️ Roadmap", "📌 Sticky Notes", "📖 Deep Dive"])

    # ----------------------------------------------------
    # TAB 1: THE PREREQUISITE ROADMAP (Mermaid.js)
    # ----------------------------------------------------
    with tab_roadmap:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Dynamic Knowledge Graph</div>", unsafe_allow_html=True)
        st.markdown("### Prerequisite Dependency Roadmap")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Interactive dependency tree visualizing concepts and logical progression.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            # Render Mermaid.js in an isolated iframe
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

        # 4-column digital sticky notes corkboard
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
    # TAB 3: IN-DEPTH REVISION NOTES (Markdown & LaTeX)
    # ----------------------------------------------------
    with tab_deepdive:
        st.markdown("<div class='micro-label' style='margin-bottom: 0.5rem;'>Comprehensive Study Guide</div>", unsafe_allow_html=True)
        st.markdown("### In-Depth Revision & Formal Notes")
        st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-bottom: 1.5rem;'>Rigorous notes, mathematical derivations, comparison matrices, and code references.</p>", unsafe_allow_html=True)

        with st.container(border=True):
            with st.expander("📚 Expand Full Revision Module", expanded=True):
                st.markdown(st.session_state.revision_notes)
