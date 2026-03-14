from fastapi import Request, HTTPException
import requests
import logging
from src.common.utils import create_app
from src.common.config import settings
import uvicorn

AUTH_URL = settings.AUTH_URL
INFRA_URL = settings.INFRA_MANAGER_URL
ID = "infra-manager"
PWD = settings.NF_CREDENTIALS.get("infra-manager", "infra-secret")
app = create_app("5G Auto-Scaling Orchestrator")
logger = logging.getLogger("Orchestrator")

def get_jwt():
    res = requests.post(AUTH_URL, data={"username": ID, "password": PWD})
    if res.status_code == 200:
        return res.json().get("access_token")
    return None

@app.post("/webhook/scale")
async def handle_alert(request: Request):
    data = await request.json()
    alerts = data.get("alerts", [])
    for alert in alerts:
        status = alert.get("status")
        name = alert.get("labels", {}).get("alertname")
        if status == "firing" and name == "HighAMFLoad":
            logger.info(f"Something's wrong: {name}. Scaling out...")
            token = get_jwt()
            if not token:
                raise HTTPException(status_code=500, detail="Could not fetch token")
            headers = {"Authorization": f"Bearer {token}"}
            # call infra de scale
            scale_res = requests.post(
                f"{INFRA_URL}/vnf/amf-v1/scale", 
                params={"flavor_name": "m1.large"}, 
                headers=headers
            )
            if scale_res.status_code == 200:
                logger.info("Scaling done")
            else:
                logger.error(f"Scale failed: {scale_res.status_code}")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
