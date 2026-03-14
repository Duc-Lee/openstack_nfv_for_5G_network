from fastapi import Request, Depends, HTTPException
from src.common.database import DatabaseManager
from src.common.auth import get_current_client
from src.common.utils import create_app
from src.common.config import settings
from sqlalchemy import Column, String, Integer
import httpx
import uvicorn

db_manager = DatabaseManager()
Base = db_manager.Base
db_manager.create_tables()
s_count = 0
UPF_URL = settings.UPF_URL
app = create_app("5G SMF")

class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(Integer, primary_key=True, index=True)
    ue_id = Column(String(15))
    assigned_ip = Column(String(15))

@app.post("/session")
async def create_session(request: Request, user: str = Depends(get_current_client), db = Depends(db_manager.get_session)):
    global s_count
    s_count += 1
    data = await request.json()
    ue_id = data.get("ue_id", "unknown")
    ip = f"10.0.0.{s_count % 254}"
    db.add(Session(ue_id=ue_id, assigned_ip=ip))
    db.commit()
    print(f"Session saved: UE {ue_id}")
    # Báo cho UPF
    headers = {"Authorization": request.headers.get("Authorization")}
    async with httpx.AsyncClient() as client:
        upf_res = await client.post(
            f"{UPF_URL}/process-data", 
            json={"ue_id": ue_id, "size_mb": 0.01}, 
            headers=headers, 
            timeout=5.0
        )
        if upf_res.status_code != 200:
            raise HTTPException(status_code=502, detail="UPF error")       
    return {
        "status": "session_ok",
        "ue_id": ue_id,
        "ip": ip
    }

@app.get("/metrics")
async def metrics():
    return f"smf_sessions {s_count}\n"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
