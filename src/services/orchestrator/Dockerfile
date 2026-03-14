FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn requests
COPY src/common ./src/common
COPY src/services/orchestrator ./src/services/orchestrator
ENV PYTHONPATH=/app
CMD ["uvicorn", "src.services.orchestrator.main:app", "--host", "0.0.0.0", "--port", "8005"]
