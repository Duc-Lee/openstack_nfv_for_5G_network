FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn python-jose[cryptography] python-multipart requests
COPY src/common ./src/common
COPY src/services/auth_service ./src/services/auth_service
ENV PYTHONPATH=/app
CMD ["uvicorn", "src.services.auth_service.main:app", "--host", "0.0.0.0", "--port", "8004"]
