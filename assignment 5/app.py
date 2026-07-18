import streamlit as st
import json
import requests
import urllib.parse
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from gtts import gTTS
import io

# --- Phase 1: The Director's Cut (UI & Config) ---
st.set_page_config(page_title="The Multi-Modal Visual Novel", page_icon="📖", layout="centered")

load_dotenv()

@st.cache_resource
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

st.title("📖 The Visual Novel Engine")
st.markdown("A dynamic, fully AI-generated Choose Your Own Adventure game.")

with st.sidebar:
    st.header("Story Settings")
    genre = st.selectbox("Story Genre", ["Fantasy", "Sci-Fi", "Mystery", "Cyberpunk", "Horror"])
    art_style = st.selectbox("Art Style", ["Cinematic", "Anime", "Watercolor", "Pixel Art", "Comic Book"])
    
    if st.button("Restart Story", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Phase 2: The Structured JSON Engine ---
system_instruction = f"""
You are the game master for a {genre} visual novel.
You must STRICTLY respond with a JSON object. Do NOT include markdown blocks like ```json.
Your JSON object MUST contain exactly these three keys:
1. "story_text": The narrative paragraph describing the current situation.
2. "image_prompt": A highly detailed, descriptive prompt for an image generator representing the scene. Do NOT include the art style here.
3. "options": A list containing 2 to 3 distinct string choices for the user's next action.
Always progress the story based on the user's latest choice.
"""

def generate_next_scene(user_prompt):
    # Store user choice in the state
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Reconstruct history for Gemini to maintain continuity
    api_history = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            api_history.append(types.Content(role="user", parts=[types.Part.from_text(text=msg["content"])]))
        elif msg["role"] == "model":
            api_history.append(types.Content(role="model", parts=[types.Part.from_text(text=msg["raw_content"])]))
            
    with st.spinner("The AI Director is writing the next scene..."):
        try:
            # Force JSON format return
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=api_history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            raw_content = response.text
            
            # The Engineering Challenge: Parse JSON string into Python dict
            data = json.loads(raw_content)
            
            story_text = data.get("story_text", "The story continues...")
            image_prompt = data.get("image_prompt", "A blank scene")
            options = data.get("options", ["Continue"])
            
            # --- Phase 4 & 5: Multi-Media & Graceful Failures ---
            
            # 1. Image Generation (Pollinations)
            full_img_prompt = f"{image_prompt}, {art_style} style, masterpiece, highly detailed"
            safe_prompt = urllib.parse.quote(full_img_prompt)
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=512"
            
            image_data = None
            try:
                res = requests.get(url, timeout=15)
                res.raise_for_status()
                image_data = res.content
            except Exception as e:
                # Graceful Failure Notification
                st.toast("Image server is busy, skipping visual...")
                
            # 2. Audio Generation (gTTS)
            audio_data = None
            try:
                tts = gTTS(text=story_text, lang='en')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                audio_data = fp.read()
            except Exception as e:
                # Graceful Failure Notification
                st.toast("TTS service failed, skipping audio...")
                
            # Save the fully processed scene to session state
            st.session_state.messages.append({
                "role": "model",
                "raw_content": raw_content,
                "story_text": story_text,
                "image_data": image_data,
                "audio_data": audio_data,
                "options": options
            })
            
        except Exception as e:
            st.error(f"Failed to generate story: {e}")
            st.session_state.messages.pop() # Remove failed user prompt so they can try again

# --- Main App Rendering ---
if len(st.session_state.messages) == 0:
    st.info("Configure your story in the sidebar, then click below to begin.")
    if st.button("Start Adventure", type="primary"):
        generate_next_scene("Start the story.")
        st.rerun()
else:
    # Render all past scenes
    for i, msg in enumerate(st.session_state.messages):
        # We optionally display the user's choice to remind them what they picked
        if msg["role"] == "user" and msg["content"] != "Start the story.":
            st.markdown(f"**You chose:** *{msg['content']}*")
            
        elif msg["role"] == "model":
            with st.container(border=True):
                # Render Image
                if msg["image_data"]:
                    st.image(msg["image_data"])
                
                # Render Text
                st.markdown(f"### {msg['story_text']}")
                
                # Render Audio
                if msg["audio_data"]:
                    st.audio(msg["audio_data"], format="audio/mp3")
                
                # --- Phase 3: Dynamic UI Generation ---
                # We ONLY render the choice buttons for the LATEST scene.
                if i == len(st.session_state.messages) - 1:
                    st.divider()
                    st.write("**What do you do next?**")
                    
                    # Dynamically loop through the options list from JSON
                    for option in msg["options"]:
                        # Give buttons a unique key using their text and index
                        if st.button(option, key=f"btn_{i}_{option}"):
                            generate_next_scene(option)
                            st.rerun()
