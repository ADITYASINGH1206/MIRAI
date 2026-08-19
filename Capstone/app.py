import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Omni-Quant Portfolio Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ANTIGRAVITY / PREMIUM UI INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Base theme override - dark, sleek */
    .stApp {
        background: radial-gradient(circle at top center, #111116 0%, #060608 100%);
        font-family: 'Outfit', sans-serif !important;
        color: #EDEDED;
    }

    /* Hide typical Streamlit chrome */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    footer { visibility: hidden; }

    /* Titles and Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em;
    }
    
    /* Title glowing effect */
    h1 {
        background: linear-gradient(180deg, #FFFFFF 0%, #A1A1AA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 32px rgba(255,255,255,0.1);
    }

    /* GLASSMORPHISM METRIC CARDS */
    [data-testid="stMetric"] {
        background: rgba(20, 20, 25, 0.3);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        /* Slight isometric 3D tilt on hover */
        transform-style: preserve-3d;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) rotateX(2deg) rotateY(-2deg);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #fff !important;
    }

    [data-testid="stMetricLabel"] {
        color: #A1A1AA !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.8rem !important;
        margin-bottom: 8px;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* FORM AND INPUT ZONES (Glassmorphism + Weightlessness) */
    [data-testid="stForm"] {
        background: rgba(25, 25, 30, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    
    /* Button overrides */
    .st-key-run-ai-btn > button {
        background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.05) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #fff !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    .st-key-run-ai-btn > button:hover {
        background: linear-gradient(180deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.08) 100%) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4) !important;
    }
    .st-key-run-ai-btn > button:active {
        transform: translateY(1px) !important;
    }

    /* Data Editor */
    .st-key-portfolio-editor {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.05) !important;
        margin-top: 3rem;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)
# ----------------------------------------

# Initialize Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ GEMINI_API_KEY not found in environment variables. AI features will be disabled.")

# Define the mock portfolio initialization function
def init_portfolio():
    if "portfolio_df" not in st.session_state:
        st.session_state.portfolio_df = pd.DataFrame({
            "Asset Ticker": ["BTC", "ETH", "AAPL", "TSLA", "NVDA"],
            "Position Size ($)": [15000.0, 8000.0, 12000.0, 5000.0, 20000.0],
        })

init_portfolio()

# Calculate current allocation (%) dynamically
def update_allocation(df):
    total_value = df["Position Size ($)"].sum()
    if total_value > 0:
        df["Current Allocation (%)"] = (df["Position Size ($)"] / total_value) * 100
    else:
        df["Current Allocation (%)"] = 0.0
    return df

# Helper to process multimodal AI input
def run_quant_analysis(image_bytes, audio_bytes, portfolio_str):
    if not API_KEY:
        return "Error: Gemini API key is missing. Please set it in your .env file."
    
    try:
        # We use the gemini-1.5-pro model for multimodal tasks
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # System prompt strategy as per instructions
        prompt = f"""
You are a ruthless, highly critical, and elite hedge fund manager. 
The user is presenting their current portfolio allocation, a screenshot of their technical setup, and dictating their market thesis via audio.

Your task:
1. Cross-reference the provided audio thesis (if transcribed/understood) with the visual chart.
2. Brutally roast the user's portfolio allocation based on the provided data.
3. Provide a strict, bulleted recovery plan to optimize their positions and risk management.

User Portfolio:
{portfolio_str}

Analyze the provided inputs and deliver your assessment.
        """
        
        contents = [prompt]
        
        # Add image if provided
        if image_bytes is not None:
            contents.append(
                {"mime_type": "image/jpeg", "data": image_bytes.getvalue()}
            )
            
        # Add audio if provided
        if audio_bytes is not None:
            # Note: Gemini 1.5 Pro natively supports audio inputs. We pass it as data.
            contents.append(
                {"mime_type": "audio/wav", "data": audio_bytes.getvalue()}
            )
            
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        return f"An error occurred during AI analysis: {str(e)}"

# --- Main UI Layout ---
st.title("📈 Omni-Quant Portfolio Terminal & Sentiment Roaster")
st.markdown("Welcome to the ultimate hedge fund dashboard. Manage your state, visualize data, and get absolutely roasted by our multimodal AI.")

# Three.js 3D Visualization via components.html
components.html(
    """
    <div id="canvas-container" style="width: 100%; height: 300px; overflow: hidden; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 30px rgba(0,0,0,0.5);"></div>
    <script type="module">
        import * as THREE from 'https://cdn.skypack.dev/three@0.136.0';
        
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);
        
        const geometry = new THREE.TorusKnotGeometry(10, 2.5, 120, 16);
        const material = new THREE.MeshBasicMaterial({ color: 0x4a90e2, wireframe: true, transparent: true, opacity: 0.8 });
        const torusKnot = new THREE.Mesh(geometry, material);
        scene.add(torusKnot);
        
        camera.position.z = 25;
        
        function animate() {
            requestAnimationFrame(animate);
            torusKnot.rotation.x += 0.005;
            torusKnot.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();
        
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
    """,
    height=310,
)

# Update allocation based on current session state
current_df = update_allocation(st.session_state.portfolio_df.copy())
total_portfolio_value = current_df["Position Size ($)"].sum()

# Dynamic KPI Cards
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    st.metric("Total Portfolio Value", f"${total_portfolio_value:,.2f}", delta="0.00%")
with kpi_col2:
    top_asset = current_df.loc[current_df["Position Size ($)"].idxmax()]["Asset Ticker"] if not current_df.empty else "N/A"
    st.metric("Top Holding", top_asset)
with kpi_col3:
    st.metric("Risk Profile", "High" if total_portfolio_value > 50000 else "Moderate")

st.divider()

# Layout: Data Editor (Left) & AI Inputs (Right)
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("📊 Portfolio Manager")
    st.markdown("Adjust your position sizes below. The allocation will update automatically.")
    
    # Use st.data_editor for dynamic adjustments
    edited_df = st.data_editor(
        current_df,
        column_config={
            "Position Size ($)": st.column_config.NumberColumn(
                "Position Size ($)",
                min_value=0.0,
                format="$%d",
                step=100.0,
            ),
            "Current Allocation (%)": st.column_config.NumberColumn(
                "Current Allocation (%)",
                format="%.2f%%",
                disabled=True,
            )
        },
        hide_index=True,
        use_container_width=True,
        key="portfolio-editor"
    )
    
    # Update session state with edited positions (dropping calculated allocation for clean state)
    if not edited_df.equals(current_df):
        st.session_state.portfolio_df = edited_df[["Asset Ticker", "Position Size ($)"]]
        st.rerun()

with col_right:
    st.subheader("🤖 AI Sentiment Roaster")
    
    # Analysis Zone wrapped in a form
    with st.form("quant_form"):
        st.markdown("**Submit your setup and thesis for a brutal AI review.**")
        
        uploaded_image = st.camera_input("Upload a screenshot of your technical setup")
        recorded_audio = st.audio_input("Dictate your market thesis")
        
        submit_button = st.form_submit_button("Run AI Quant Analysis", type="primary", key="run-ai-btn")

    if submit_button:
        with st.spinner("Analyzing portfolio, chart, and thesis... Brace yourself."):
            portfolio_string = current_df.to_string(index=False)
            ai_response = run_quant_analysis(uploaded_image, recorded_audio, portfolio_string)
            
            with st.expander("View System Logs & Analysis", expanded=True):
                st.write(ai_response)
