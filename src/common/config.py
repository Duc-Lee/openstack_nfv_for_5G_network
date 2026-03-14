import os

SECRET_KEY = "5g-core-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# Dia chi cac service 
AUTH_URL = "http://auth:8004/token"
AMF_URL = "http://amf:8000"
SMF_URL = "http://smf:8001"
UPF_URL = "http://upf:8002"
INFRA_MANAGER_URL = "http://infra:8003"

# Ket noi Postgres
DB_USER = os.getenv("DB_USERNAME", "duckle")
DB_PASS = os.getenv("DB_PASSWORD", "anhduc2005")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "fiveg_core")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# User pass cho NF
NF_CREDENTIALS = {
    "amf": "amf-secret",
    "smf": "smf-secret",
    "upf": "upf-secret",
    "infra": "infra-secret"
}

class Settings:
    def __init__(self):
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
        self.AUTH_URL = AUTH_URL
        self.AMF_URL = AMF_URL
        self.SMF_URL = SMF_URL
        self.UPF_URL = UPF_URL
        self.INFRA_MANAGER_URL = INFRA_MANAGER_URL
        self.DATABASE_URL = DATABASE_URL
        self.NF_CREDENTIALS = NF_CREDENTIALS

settings = Settings()

