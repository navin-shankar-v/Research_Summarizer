import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie
import time

# Optional: pip install streamlit-lottie

# ------------------- STYLING -------------------
st.set_page_config(page_title="Automated Research Summarization", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0f1116;
        color: #f0f0f5;
    }
    .title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #00b4d8;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #adb5bd;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #00b4d8;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.6rem 1.2rem;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0096c7;
        transform: scale(1.05);
    }
    .result-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-top: 1rem;
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.2);
    }
    .section-title {
        color: #90e0ef;
        font-weight: 600;
        font-size: 1.2rem;
        border-bottom: 1px solid #00b4d8;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown('<div class="title">Automated Research Summarization</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered summarizer for extracting insights from academic research</div>', unsafe_allow_html=True)

# ------------------- INPUTS -------------------
topic = st.text_input("Enter your topic", placeholder="e.g., Blockchain, Smart Watches, Federated Learning")
n_papers = st.slider("Number of papers to include", 3, 12, 5)
api_url = "http://localhost:8000/api/summarize"

# ------------------- SUBMIT -------------------
if st.button("🚀 Generate Summary") and topic:
    with st.spinner("Gathering papers and generating insights... This may take a minute ⏳"):
        try:
            resp = requests.post(api_url, json={"query": topic, "n_papers": n_papers, "sources": ["arxiv"]}, timeout=180)
            data = resp.json()

            st.success("✅ Summary generated successfully!")
            summary = data.get("summary", {})
            
            # ------------------- OUTPUT CARDS -------------------
            with st.container():
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                # Summary
                st.markdown('<div class="section-title">📘 Summary</div>', unsafe_allow_html=True)
                for p in summary.get("paragraphs", []):
                    st.markdown(f"- {p}")

                # What's New
                st.markdown('<div class="section-title">🌟 What\'s New</div>', unsafe_allow_html=True)
                for point in summary.get("whats_new", []):
                    st.markdown(f"✅ {point}")

                # Open Problems
                st.markdown('<div class="section-title">⚙️ Open Problems</div>', unsafe_allow_html=True)
                for prob in summary.get("open_problems", []):
                    st.markdown(f"🔍 {prob}")

                # Top 5 Papers
                st.markdown('<div class="section-title">📑 Top 5 Papers</div>', unsafe_allow_html=True)
                for paper in summary.get("top5_papers", []):
                    st.markdown(f"🔗 **[{paper.get('title','Untitled')}]({paper.get('url','#')})**")

                st.markdown('</div>', unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Try again or reduce the number of papers.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

else:
    st.info("Enter a topic and click **Generate Summary** to begin.")

# ------------------- FOOTER -------------------
st.markdown("""
<hr style="margin-top:3rem; border: 0.5px solid #00b4d8; opacity:0.2;">
<p style="text-align:center; font-size:0.9rem; color:#adb5bd;">
Built with ❤️ using Streamlit & FastAPI | Powered by Ollama / GPT | © 2025 Navinshankar G.V.
</p>
""", unsafe_allow_html=True)
