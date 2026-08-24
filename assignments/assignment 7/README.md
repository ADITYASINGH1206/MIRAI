<div align="center">

<h1 align="center">Life-OS: Digital Wellbeing Dashboard 🧘</h1>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?size=22&duration=3000&color=36BCF7&center=true&vCenter=true&width=600&lines=Reclaim+Your+Screen+Time;AI-Powered+Life+Coaching;Data-Driven+Productivity" />
</p>

---

### 🚀 Overview
The **Life-OS Dashboard** is a data-driven Streamlit application designed to combat digital addiction. It analyzes daily screen time usage and leverages the Gemini API to act as a brutally honest, holistic life coach. 

---

### ⚡ Key Features
- **📊 Interactive Data Visualization**: 14-day trend analysis and daily snapshot KPIs.
- **🧠 The AI Data Bridge**: Aggregates Pandas DataFrame statistics and converts them into structured JSON for LLM analysis.
- **🧘 Holistic Life Coaching**: Gemini evaluates your habits and suggests real-world, physical replacements for digital doomscrolling.
- **🎨 The Guilt-Trip Avatar (Innovation)**: Dynamically generates an AI avatar using Pollinations based on how productive or lazy your day was.

---

### 🛠️ Tech Stack

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

</div>

---

### 🚀 Installation & Deployment

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   Create a `.env` file and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_key_here
   ```
4. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```

*Note: For public deployment (e.g. Streamlit Community Cloud), ensure your API keys are stored in the platform's Secrets management system and never push the `.env` file!*

</div>
