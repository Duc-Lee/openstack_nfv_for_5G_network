from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt
import uvicorn
from src.common.utils import create_app
from src.common.config import settings

app = create_app("5G Auth Service")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = form_data.username
    pw = form_data.password
    if user not in settings.NF_CREDENTIALS or settings.NF_CREDENTIALS[user] != pw:
        raise HTTPException(
            status_code=401,
            detail="Wrong NF login info",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": user, "scope": "sba:access"})
    return {"access_token": token, "token_type": "bearer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
