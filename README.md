# ▓▒░ STUDY OS // Precision Learning Platform ░▒▓

> **Status:** `SYSTEM NOMINAL` | **Build:** `STITCH-1.4.2` | **Telemetry:** `ONLINE`

**STUDY OS** is an AI-powered, multimodal precision learning platform developed for the MirAI School of Technology Capstone. It leverages Streamlit, Pandas, and the Gemini AI Engine to dynamically synthesize study materials into high-retention flashcards, matrix evaluations, and knowledge topologies.

Designed with a strict "Cinematic Precision" design system (Stitch UI), it ditches standard interfaces for a glassmorphic, terminal-aesthetic architecture tailored for deep work.

---

## ⚡ CORE MODULES

* **Explain & Memorize (Flashcards):** 
  Input any technical topic (e.g., "Supervised vs Unsupervised Learning"), and the Gemini API automatically generates a comparative analysis alongside 5 precise "Memory Vectors" (Flashcards).
* **Quiz Builder (Evaluation Matrix):** 
  Inject raw, unstructured lecture transcripts into the parser. The engine synthesizes a 5-question multiple-choice quiz and tracks your telemetry in a mock state container, preventing memory loss.
* **Analytics & Roadmap (System Telemetry):** 
  A high-fidelity dashboard built with Pandas. Features dynamic KPI tracking, a Github-style 365-day Activity Signal heatmap, and a fully interactive Mermaid.js Knowledge Topology graph.
* **My Notes (Personal Memory):** 
  A dedicated module for unstructured user notes with built-in timestamping and state persistence.
* **Multimodal Ingestion:** 
  Native support for text outlines, voice dictation (`st.audio_input`), and whiteboard scans (`st.camera_input`) routed directly to the AI engine for synthesis.

---

## 🛠 ARCHITECTURE & STACK

* **Frontend Engine:** Streamlit `1.42.0` (with severe CSS overrides for Stitch Design Language)
* **LLM Engine:** Google Gemini Flash (`google-generativeai`)
* **State Management:** `st.session_state` (Ephemeral routing, metric tracking, and persistent quiz/note arrays)
* **Data Processing:** Pandas & Numpy (Telemetry mock generation & DataFrames)
* **Typography:** `Cascadia Mono`, `SFMono-Regular`

---

## 🚀 SETUP INSTRUCTIONS (LOCAL DEVELOPMENT)

### 1. Clone & Environment
```bash
git clone https://github.com/ADITYASINGH1206/MIRAI.git
cd MIRAI/Capstone
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: `requirements.txt` is perfectly configured for cloud deployment with zero local dependencies).*

### 3. Configure API
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Ignite Sequence
```bash
streamlit run app.py
```
> Application will be active at `http://localhost:8503`

---

## 🌐 DEPLOYMENT (LIVE APP)

The application is engineered for immediate deployment on **Streamlit Community Cloud**.

**Live Link:** `[PENDING DEPLOYMENT — Insert Streamlit Cloud URL here]`

*(See `system_design.md` for in-depth architecture and data flow).*
