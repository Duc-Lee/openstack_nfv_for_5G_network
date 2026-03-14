from fastapi import Request, Depends
import os
from src.common.auth import get_current_client
from src.common.utils import create_app
import uvicorn

app = create_app("5G UPF")
total_data = 0

@app.post("/process-data")
async def process_data(request: Request, user = Depends(get_current_client)):
    global total_data
    data = await request.json()
    ue_ip = data.get("ue_ip", "unknown")
    size = data.get("payload_size", 0) 
    total_data += size / (1024 * 1024)
    print(f"UPF: Pushing {size} KB for UE {ue_ip}")
    return {
        "status": "ok",
        "inst": os.getenv("HOSTNAME", "upf-1")
    }

@app.get("/metrics")
async def metrics():
    return f"upf_data_gb {total_data}\n"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
