FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn python-jose[cryptography] requests
COPY src/common ./src/common
COPY src/services/upf ./src/services/upf

ENV PYTHONPATH=/app
# Bind to multiple interfaces using uvicorn at runtime
# eth0 for Management, eth1 for Control/User Plane
CMD ["uvicorn", "src.services.upf.main:app", "--host", "0.0.0.0", "--port", "8002"]
