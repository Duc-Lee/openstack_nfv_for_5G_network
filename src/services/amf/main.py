from fastapi import Request, HTTPException, Depends
import time
from sqlalchemy import Column, String
import httpx
from src.common.database import DatabaseManager
from src.common.auth import get_current_client
from src.common.utils import create_app
from src.common.config import settings
import uvicorn

db_manager = DatabaseManager()
Base = db_manager.Base
app = create_app("5G AMF")

class Subscriber(Base):
    __tablename__ = "subscribers"
    imsi = Column(String(15), primary_key=True, index=True)
    key = Column(String(32))
    op = Column(String(32))

db_manager.create_tables()
count = 0
SMF_URL = settings.SMF_URL

@app.post("/attach")
async def attach(request: Request, user: str = Depends(get_current_client), db = Depends(db_manager.get_session)):
    global count
    count += 1
    data = await request.json()
    ue_id = data.get("ue_id", "unknown")
    sub = db.query(Subscriber).filter(Subscriber.imsi == ue_id).first()
    if not sub:
        print(f"Attach rejected: UE {ue_id} not in DB")
        raise HTTPException(status_code=403, detail="Can't find subscriber")
    print(f"Attach success: UE {ue_id} is ok")
    # Gọi SMF
    headers = {"Authorization": request.headers.get("Authorization")}
    async with httpx.AsyncClient() as client:
        smf_res = await client.post(f"{SMF_URL}/session", json={"ue_id": ue_id}, headers=headers, timeout=5.0)
        if smf_res.status_code != 200:
            raise HTTPException(status_code=502, detail="Can't connect to SMF")
        smf_data = smf_res.json()       
    return {
        "status": "attached",
        "ue_id": ue_id,
        "ip": smf_data.get("assigned_ip", "none"),
        "ts": time.time()
    }

@app.get("/metrics")
async def metrics():
    return f"amf_requests {count}\n"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
