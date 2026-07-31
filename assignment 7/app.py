import streamlit as st
import pandas as pd
import requests
import urllib.parse
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

st.set_page_config(page_title="Life-OS Dashboard", page_icon="🧘", layout="wide")
load_dotenv()

# --- Initialize Gemini ---
@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found in .env")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# --- Phase 1: Data Pipeline ---
@st.cache_data
def load_data():
    df = pd.read_csv("screentime.csv")
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("screentime.csv not found. Please ensure the synthetic data script was run.")
    st.stop()

# --- Phase 2: Command Center UI ---
st.title("🧘 Life-OS Wellbeing Dashboard")
st.markdown("Monitor your digital health and get brutal-but-fair coaching from AI.")

st.sidebar.header("Controls")
available_dates = sorted(list(df['Date'].unique()))
selected_date = st.sidebar.selectbox("Select Date", available_dates, index=len(available_dates)-1)
daily_goal = st.sidebar.slider("Daily Goal (Minutes)", min_value=60, max_value=600, value=240, step=30)

# Filter data
df_today = df[df['Date'] == selected_date]
total_mins_today = int(df_today['Minutes_Used'].sum())
most_used_app = df_today.groupby('App_Name')['Minutes_Used'].sum().idxmax()
delta_val = total_mins_today - daily_goal

# KPI Row
st.subheader("Daily Snapshot")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Screen Time", f"{total_mins_today} mins")
with col2:
    st.metric("Most Used App", most_used_app)
with col3:
    # We want a positive delta to be red (over goal), so we pass delta_color="inverse"
    # But wait, in Streamlit, delta is normally green when positive. 
    # To make negative values green (under goal) and positive red (over goal), we use "inverse".
    # Since a positive delta_val means they went OVER the goal, we want it to be red.
    st.metric("Vs. Daily Goal", f"{delta_val} mins", delta=-delta_val, delta_color="normal")
    # Actually, delta_color="inverse" makes positive values red and negative green.
    # Let's just use delta_val and inverse.
    # Wait, if I pass `delta=-delta_val`, it means passing a negative number when over goal. 
    # The default is green for positive, red for negative. 
    # If they are OVER goal (delta_val > 0), passing -delta_val makes it red.

# Trend Visualization
st.subheader("14-Day Usage Trends")
daily_totals = df.groupby('Date')['Minutes_Used'].sum().reset_index()
daily_totals = daily_totals.set_index('Date')
st.bar_chart(daily_totals)

# --- Phase 3 & 4: AI Coaching & Guilt-Trip Avatar ---
st.divider()
st.subheader("🧠 The AI Life Coach")

# The Data Bridge
category_totals = df_today.groupby('Category')['Minutes_Used'].sum().to_dict()
usage_summary_str = json.dumps(category_totals, indent=2)

system_prompt = f"""
You are a personalized, brutal-but-fair productivity and holistic life coach.
The user has provided their screen time data for the day across different categories:
{usage_summary_str}
Their daily goal was {daily_goal} minutes.

Your job is to:
1. Analyze their usage. Do NOT just say "use your phone less".
2. Suggest physical, real-world replacements. If they spent hours on Social Media, suggest reclaiming that time for physical fitness, meal prepping, or reading. If they spent it on Education/Coding, praise them but remind them to rest their eyes.
3. Determine a 'status': either 'Good' or 'Bad' based on if they exceeded their goal or wasted time.
4. Generate a highly descriptive image prompt (an avatar) representing their day (e.g. "a lazy zombie staring at a glowing rectangle in a dark room" for a bad day, or "a focused cyber-warrior meditating" for a good day).

You MUST strictly return a JSON object with these keys:
- "advice": Your detailed coaching paragraph.
- "status": "Good" or "Bad".
- "avatar_prompt": The descriptive image prompt.
"""

if st.button("Get Today's Coaching", type="primary"):
    with st.spinner("Analyzing your digital soul..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Analyze my day and give me my avatar.",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            
            data = json.loads(response.text)
            advice = data.get("advice", "Error fetching advice.")
            status = data.get("status", "Bad")
            avatar_prompt = data.get("avatar_prompt", "a blank screen")
            
            # Phase 4: Fetch Innovation Deliverable (Guilt-Trip Avatar)
            safe_avatar_prompt = urllib.parse.quote(f"{avatar_prompt}, masterpiece, highly detailed, dramatic lighting, cinematic")
            image_url = f"https://image.pollinations.ai/prompt/{safe_avatar_prompt}?width=512&height=512"
            
            img_res = requests.get(image_url, timeout=15)
            if img_res.status_code == 200:
                avatar_img = img_res.content
            else:
                avatar_img = None
                
            # Render the results
            st.markdown("### Your Evaluation")
            col_img, col_text = st.columns([1, 2])
            
            with col_img:
                if avatar_img:
                    st.image(avatar_img, caption="Your Daily Avatar", use_container_width=True)
                else:
                    st.warning("Avatar generation failed.")
                    
            with col_text:
                if status == "Good":
                    st.success(advice)
                else:
                    st.error(advice)
                    
        except Exception as e:
            st.error(f"Failed to generate coaching insights: {e}")
