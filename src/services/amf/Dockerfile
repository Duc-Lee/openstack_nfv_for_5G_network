FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] requests
COPY src/common ./src/common
COPY src/services/amf ./src/services/amf
ENV PYTHONPATH=/app
CMD ["uvicorn", "src.services.amf.main:app", "--host", "0.0.0.0", "--port", "8000"]
