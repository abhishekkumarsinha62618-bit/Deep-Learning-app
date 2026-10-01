FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt-lists/*

COPY backend/requirements.txt backend_reqs.txt
COPY frontend/requirements.txt frontend_reqs.txt

RUN pip install --no-cache-dir -r backend_reqs.txt
RUN pip install --no-cache-dir -r frontend_reqs.txt

COPY . /app

EXPOSE 8000

# FastAPI backend port 8001 par chalega, aur Streamlit main port 8000 par host hoga
CMD uvicorn backend.app:app --host 127.0.0.1 --port 8001 & streamlit run frontend/main.py --server.port 8000 --server.address 0.0.0.0