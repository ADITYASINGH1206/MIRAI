# STUDY OS // System Design & Architecture Document

## 1. System Architecture Overview

Study OS uses a monolithic, state-driven architecture built exclusively on **Streamlit** (`app.py`). It is designed to emulate a SPA (Single Page Application) by utilizing `st.session_state` to route between "pages" (Explain & Memorize, Quiz Builder, Analytics, Notes) without triggering full browser reloads, preserving transient data in memory.

### Architecture Diagram (Mermaid)

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#1E1E1E,stroke:#4CAF50,stroke-width:2px,color:#fff;
    classDef state fill:#2B3A42,stroke:#29B6F6,stroke-width:2px,color:#fff;
    classDef ai fill:#3E2723,stroke:#FF7043,stroke-width:2px,color:#fff;
    classDef view fill:#424242,stroke:#BDBDBD,stroke-width:1px,color:#fff;

    %% Nodes
    User([User Input: Text / Audio / Camera]):::client
    UI[Streamlit Front-End Interface]:::client
    
    subState[(st.session_state)]:::state
    
    Pipeline[LLM Pipeline Controller]:::ai
    Gemini[Google Gemini API]:::ai
    
    subgraph View Routing
        Page_Explain[Explain & Memorize View]:::view
        Page_Quiz[Quiz Builder View]:::view
        Page_Analytics[Analytics Dashboard]:::view
        Page_Notes[My Notes Module]:::view
    end

    %% Flow
    User -->|Interaction| UI
    UI -->|Updates State| subState
    subState -->|Triggers| Pipeline
    Pipeline -->|REST/gRPC| Gemini
    Gemini -->|JSON/Markdown Response| Pipeline
    Pipeline -->|Persists Data| subState
    
    subState -->|Renders| View Routing
    View Routing --> UI
```

---

## 2. Data Flow & State Management

**Goal:** Ensure zero memory loss between component interactions and simulate multi-page routing natively.

1. **Initialization (`init_state()`)**: On boot, the application initializes highly structured default schemas inside `st.session_state` (e.g., arrays for `sticky_notes`, metrics for `telemetry`, empty strings for `quiz_questions`).
2. **Event Triggers**: The user interacts with `st.form_submit_button` or sidebar HTML anchors.
3. **State Updates**: Forms immediately update variables in `st.session_state` rather than triggering standalone python variables.
4. **Re-Renders**: By calling `st.rerun()`, the monolithic script reads the newly updated `st.session_state` from the top, resolving routing logic (`if current_page == 'explain': ...`) to render the correct UI.

---

## 3. API Integration Strategy (Google Gemini)

We utilize the `google-generativeai` SDK to communicate with the Gemini Flash model. To prevent "generic chatbot" outputs, the system forces strict constraints:

* **System Instructions:** The `model` object is initialized with highly detailed system prompts (e.g., instructing it to act as "Study OS", outputting exclusively JSON).
* **Deterministic Output Parsing:** 
    * We employ the `response_mime_type="application/json"` config parameter within the `GenerationConfig`.
    * Prompts are formatted using Python `f-strings` to securely inject user inputs inside predefined JSON schema requests (e.g., `{"q": "question", "a": "answer"}`).
* **Multimodal Ingestion Pipeline:** 
    * The architecture handles multi-modal inputs natively via Streamlit's `st.audio_input` and `st.camera_input`.
    * Base64 encoded audio/images are appended to the payload directly before transmission to the Gemini engine for synthesis into structured flashcards.

---

## 4. Logic Modules & UI Components

* **Stitch Design Language (CSS Overrides):** Instead of standard Streamlit components, `st.markdown(unsafe_allow_html=True)` injects custom CSS variables, overriding native Streamlit classes (`stApp`, `stSidebar`) to achieve a glassmorphic, terminal aesthetic.
* **Master Ingestion Stream:** A sticky form at the bottom of `app.py` leveraging `st.form`. This batches user inputs and executes a single AI call to minimize rate limiting and latency.
* **Analytics Data Visualization:** Utilizes `pandas.DataFrame` and `numpy` to generate simulated telemetry data, visualized natively through Streamlit's fast charting utilities (`st.bar_chart` equivalents) and `components.html` to inject raw Mermaid.js topologies.
