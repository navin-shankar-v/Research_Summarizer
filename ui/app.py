import streamlit as st
import requests
import os

# Base API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")
api_url = f"{API_URL}/api/summarize"

st.set_page_config(page_title="Automated Research Summarization", layout="wide")

# ------------------- STYLING -------------------
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

# ------------------- SUBMIT -------------------
if st.button("🚀 Generate Summary") and topic:
    with st.spinner("Gathering papers and generating insights... This may take a minute ⏳"):
        try:
            resp = requests.post(
                api_url,
                json={"query": topic, "n_papers": n_papers, "sources": ["arxiv"]},
                timeout=180
            )

            if resp.status_code != 200:
                st.error(f"Server Error: {resp.text}")
                st.stop()

            data = resp.json()
            summary = data.get("summary", {}) or {}
            scores = data.get("eval", {}) or {}
            papers = data.get("papers", []) or {}

            st.success("✅ Summary generated successfully!")

            # ------------------- TABS -------------------
            tab_summary, tab_details, tab_papers = st.tabs(
                ["📘 Summary", "📊 Details & Structure", "📑 Papers"]
            )

            # ===== TAB: SUMMARY =====
            with tab_summary:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                # Evaluation metrics
                st.markdown('<div class="section-title">📊 Evaluation</div>', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Overall", f"{scores.get('overall', 0):.2f}")
                c2.metric("Coverage", f"{scores.get('coverage', 0):.2f}")
                c3.metric("Depth", f"{scores.get('depth', 0):.2f}")
                c4.metric("Structure", f"{scores.get('structure', 0):.2f}")

                # Deep paragraphs
                st.markdown('<div class="section-title">📘 Deep Summary</div>', unsafe_allow_html=True)
                for p in summary.get("paragraphs", []):
                    st.markdown(f"- {p}")

                st.markdown('</div>', unsafe_allow_html=True)

            # ===== TAB: DETAILS =====
            with tab_details:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                mapping = {
                    "🔎 Key Findings": "key_findings",
                    "⚠️ Limitations": "limitations",
                    "🚀 Future Work": "future_work",
                    "🧪 Methods": "methods",
                    "✨ What's New": "whats_new",
                    "🧩 Open Problems": "open_problems",
                }

                for title, key in mapping.items():
                    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
                    for item in summary.get(key, []):
                        st.markdown(f"- {item}")

                st.markdown('</div>', unsafe_allow_html=True)

            # ===== TAB: PAPERS =====
            with tab_papers:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)

                st.markdown('<div class="section-title">📑 Top 5 Papers</div>', unsafe_allow_html=True)
                for paper in summary.get("top5_papers", []):
                    st.markdown(f"🔗 **[{paper.get('title')}]({paper.get('url')})**")

                st.markdown('<div class="section-title">📚 Retrieved Papers</div>', unsafe_allow_html=True)
                for i, p in enumerate(papers, start=1):
                    st.markdown(f"### [{i}] {p.get('title','Untitled')} ({p.get('year','')})")
                    st.markdown(f"- Authors: {p.get('authors','N/A')}")
                    st.markdown(f"- URL: {p.get('url','N/A')}")
                    st.markdown("---")

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
