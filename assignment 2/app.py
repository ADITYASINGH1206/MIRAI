import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

st.set_page_config(page_title="PersonaSphere", page_icon="🎭")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("🎭 PersonaSphere")

with st.sidebar:
    personality = st.selectbox(
        "Select Personality:",
        ["Sarcastic Tech Support", "Motivational Coach", "Friendly Teacher", "AI Assistant"]
    )
    creativity = st.slider("Creativity", 0.0, 2.0, 0.7, 0.1)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "curr_p" not in st.session_state:
    st.session_state.curr_p = personality
if "curr_c" not in st.session_state:
    st.session_state.curr_c = creativity

if st.session_state.curr_p != personality or st.session_state.curr_c != creativity:
    st.session_state.messages = []
    st.session_state.curr_p = personality
    st.session_state.curr_c = creativity

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Say something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    api_history = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        api_history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

    sys_inst = f"You are acting exclusively as a {personality}. Always stay in character."

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=api_history,
                config=types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    temperature=creativity,
                )
            )
            answer = response.text
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")
            st.session_state.messages.pop()
