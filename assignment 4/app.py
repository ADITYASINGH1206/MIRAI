import streamlit as st
import requests
import random
import urllib.parse

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="centered")

st.title("🎨 AI Image Studio")
st.markdown("Transform your imagination into visual art instantly!")

# --- UI Setup ---
st.sidebar.title("Settings")
art_style = st.sidebar.selectbox(
    "Art Style", 
    ["Realistic", "Anime", "Cyberpunk", "Watercolor", "Oil Painting", "3D Render"]
)

# Sliders that were previously "broken"
width = st.sidebar.slider("Image Width", 256, 1024, 512, step=64)
height = st.sidebar.slider("Image Height", 256, 1024, 512, step=64)

# Task 3: The "Magic Enhance" Toggle
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# Task 4: The "Surprise Me!" Feature Setup
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A gigantic ancient tree with glowing blue leaves",
    "A retro-futuristic flying car over a 1950s diner",
    "A steampunk submarine exploring a coral reef"
]

prompt = st.text_input("Enter your prompt:", "A majestic lion standing on a cliff")

# Add a row of buttons
col1, col2 = st.columns([1, 1])
with col1:
    generate_btn = st.button("Generate Image", type="primary")
with col2:
    # Task 4: Surprise Me Button
    surprise_btn = st.button("🎲 Surprise Me!")

# Logic Execution
if generate_btn or surprise_btn:
    
    # Override prompt if Surprise Me is clicked
    if surprise_btn:
        prompt = random.choice(surprise_prompts)
        st.info(f"Surprise Prompt: {prompt}")

    if prompt.strip():
        with st.spinner("Painting your imagination... (This may take a moment)"):
            
            # Base prompt with style
            full_prompt = f"{prompt}, in {art_style} style"

            # Task 3: Magic Enhance Logic
            if magic_enhance:
                full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

            # Clean the string for the URL
            safe_prompt = urllib.parse.quote(full_prompt)

            # Task 1: The Broken Sliders Fix (URL Parameters)
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}"

            try:
                # Fetch image from the AI API
                response = requests.get(url)
                if response.status_code == 200:
                    image_data = response.content
                    
                    # Display the image
                    st.image(image_data, caption=full_prompt, use_container_width=True)

                    # Task 2: The File Extension Fix
                    st.download_button(
                        label="⬇️ Download Full Resolution Image",
                        data=image_data,
                        file_name=f"{art_style}_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("Failed to generate image. The server might be busy.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt first!")
