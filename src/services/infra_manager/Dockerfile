FROM python:3.10-slim

WORKDIR /app

COPY main.py .

RUN pip install fastapi uvicorn openstacksdk python-jose[cryptography]

# Use ENV variables for OpenStack authentication
ENV OS_AUTH_URL=""
ENV OS_PROJECT_NAME=""
ENV OS_USERNAME=""
ENV OS_PASSWORD=""
ENV OS_REGION_NAME=""

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
