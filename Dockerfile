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

EXPOSE 8000 8501

CMD uvicorn backend.app:app --host 0.0.0.0 --port 8000 & streamlit run frontend/main.py --server.port 8501 --server.address 0.0.0.0