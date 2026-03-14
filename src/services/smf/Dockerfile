FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] requests
COPY src/common ./src/common
COPY src/services/smf ./src/services/smf
ENV PYTHONPATH=/app
CMD ["uvicorn", "src.services.smf.main:app", "--host", "0.0.0.0", "--port", "8001"]
