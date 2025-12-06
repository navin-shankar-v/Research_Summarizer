# 🚀 Automated Research Summarizer + Evaluator

AI-powered system to extract deep insights from scientific research papers, evaluate summary quality, and track model runs with MLflow.

Built using **FastAPI**, **Streamlit**, **Ollama/GPT**, and **MLflow**.

---

# 📌 **1. Project Overview**

This project automates academic research understanding.
Given a topic (e.g., *Federated Learning*, *Blockchain Security*, *Smartwatch Health Analytics*), it:

### ✅ **Searches research papers**

From ArXiv (more sources can be added later)

### ✅ **Generates a deep scientific literature review**

The summarizer produces:

* Multi-paragraph synthesis
* Key findings
* Methods
* Limitations
* Future work
* What’s new
* Open problems
* Top 5 recommended papers

### ✅ **Evaluates the summary**

A second LLM checks:

* Depth
* Accuracy
* Novelty
* Coverage
* Coherence

Output → A **score (1–10)** + diagnostic feedback.

### ✅ **Tracks model runs using MLflow**

Every summarization run logs:

* Model used
* Prompt
* Tokens used
* Evaluation score
* Latency
* Output artifacts

---

# 🧱 **2. Tech Stack**

| Layer               | Technology                   |
| ------------------- | ---------------------------- |
| Backend             | FastAPI                      |
| Frontend            | Streamlit                    |
| LLM Providers       | OpenAI GPT (default), Ollama |
| Evaluation          | LLM-based grading agent      |
| Experiment Tracking | MLflow                       |
| Paper Retrieval     | ArXiv API                    |
| Orchestration       | Python                       |

---

# 📂 **3. Folder Structure**

```
auto-research/
│── api/
│   ├── main.py                # FastAPI entrypoint
│   ├── routers/
│   │     └── summarize.py     # Summarization API route
│── agents/
│   ├── _llm.py                # GPT/Ollama wrapper
│   ├── summarizer.py          # Deep scientific summarizer
│   ├── evaluator.py           # Summary evaluation agent
│   ├── tracking.py            # MLflow tracking utilities
│── config/
│   ├── settings.py            # Env variable loading (Pydantic)
│   ├── settings.example.env   # Example .env (NO KEYS)
│── frontend/
│   ├── app.py                 # Streamlit UI
│── requirements.txt
│── README.md
```

---

# 🔐 **4. How to Add Your OpenAI API Key (Securely)**

### **STEP 1 — Create your `.env` file**

Inside **config/** create a file named:

```
config/.env
```

Add:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
HOST=0.0.0.0
PORT=8000
```

### ❗ IMPORTANT: Do NOT commit your `.env` file.

You already have `.gitignore` rules preventing this.

---

# 🤖 **5. Switching Between GPT and Ollama**

### To use **GPT**:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

### To use **Ollama (local & free)**:

```
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=http://localhost:11434
```

Then run:

```
ollama pull llama3.1:8b
ollama serve
```

---

# 🏃‍♂️ **6. Running Backend Locally (FastAPI)**

### Install Python packages:

```
pip install -r requirements.txt
```

### Make sure `.env` is correctly set:

```
export $(grep -v '^#' config/.env | xargs)
```

### Start API server:

```
uvicorn api.main:app --reload --port 8000
```

If successful:

```
http://localhost:8000/docs
```

You should see the FastAPI Swagger UI.

---

# 🖥️ **7. Running Frontend Locally (Streamlit)**

Go to `frontend/`:

```
cd frontend
streamlit run app.py
```

Open:

```
http://localhost:8501
```

You should now see:

✔ Topic input
✔ Slider for paper count
✔ Summary generation
✔ Evaluation score
✔ Deep research analysis

---

# 📊 **8. MLflow Tracking**

To start MLflow UI:

```
mlflow ui --port 5000
```

Open:

```
http://localhost:5000
```

Every summarization run logs:

* Model provider
* Prompt
* Tokens
* Summary JSON
* Evaluation score
* Latency
* Timestamp

This allows you to compare GPT vs Ollama vs settings.

---

# 🔥 **9. Example `.env` (safe version)**

```
# LLM Provider: openai OR ollama
LLM_PROVIDER=openai

# OpenAI settings
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1

# Ollama settings
OLLAMA_MODEL=llama3.1:8b
OLLAMA_HOST=http://localhost:11434

HOST=0.0.0.0
PORT=8000
```

---

# 🧪 **10. Testing Your API Manually**

```
curl http://localhost:8000/api/summarize \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "federated learning", "n_papers": 5, "sources":["arxiv"]}'
```

---

# 📘 **11. Product Explanation (Simple Non-Tech Version)**

This tool helps students, researchers, and engineers quickly understand scientific literature.

Instead of reading 20+ academic papers, the system:

1. Finds the most relevant papers
2. Reads them
3. Writes a clear multi-paragraph literature review
4. Extracts key technical insights
5. Identifies limitations & future work
6. Evaluates the quality of the summary
7. Logs everything in MLflow

It saves **hours of manual paper reading** and generates a **research-ready summary in minutes**.

---

# 🚀 **12. Product Explanation (Technical Version)**

The system functions as a multi-agent AI pipeline:

### **Agent 1 — Research Retriever**

Fetches top papers from ArXiv based on semantic matching.

### **Agent 2 — Deep Summarizer**

Uses an LLM (GPT/Ollama) to:

* synthesize ideas
* compare model architectures
* extract fine-grained technical insights
* identify limitations, benchmarks, datasets
* propose research directions

### **Agent 3 — Evaluator**

Grades the summarizer output (1–10) based on:

* depth
* accuracy
* citation correctness
* novelty
* technical coherence

### **Agent 4 — Tracker**

Stores every run in **MLflow** for reproducibility.

---

# 🎯 Final Notes

* You MUST keep `.env` private
* Never push API keys
* Your project is now production-ready
* Hosting can be added later (Render / Railway / Fly.io / EC2)
