from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from src.common.config import settings

class Authenticator:
    def __init__(self, token_url: str = settings.AUTH_URL, secret_key: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)
        self.secret_key = secret_key
        self.algorithm = algorithm
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            client_id: str = payload.get("sub")
            if client_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return client_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

auth = Authenticator() 
async def get_current_client(token: str = Depends(auth.oauth2_scheme)):
    return auth.verify_token(token)
