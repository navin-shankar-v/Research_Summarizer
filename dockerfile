# Use a slim Python base image
FROM python:3.10-slim

# Basic envs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Workdir inside the container
WORKDIR /app

# System deps (lightweight)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Default envs (can be overridden by --env-file / -e)
ENV HOST=0.0.0.0 \
    PORT=8000 \
    API_URL=http://localhost:8000

# Expose backend + UI ports
EXPOSE 8000 8501

# Run FastAPI (uvicorn) in the background and Streamlit in the foreground
CMD ["bash", "-c", "\
uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0 \
"]
