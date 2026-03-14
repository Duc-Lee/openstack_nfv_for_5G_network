from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import openstack
import logging
from src.common.config import settings
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Infra")
app = FastAPI(title="NFV Infra Manager")
SECRET = settings.SECRET_KEY
ALGO = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.AUTH_URL}")

async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        uid = payload.get("sub")
        if not uid:
            raise HTTPException(status_code=401, detail="Token's no good")
        return uid
    except JWTError:
        raise HTTPException(status_code=401, detail="Auth failed")
# Ket noi openstack
def get_conn():
    return openstack.connect(cloud='openstack') 

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/resources/quota")
async def get_quota():
    conn = get_conn()
    compute = conn.compute.get_limits()
    storage = conn.block_storage.get_limits()
    return {
        "compute": {
            "used": compute.absolute.total_cores_used,
            "max": compute.absolute.max_total_cores
        },
        "storage": {
            "used": storage.absolute.total_gigabytes_used,
            "max": storage.absolute.max_total_gigabytes
        }
    }

@app.get("/storage/volumes")
async def list_volumes():
    conn = get_conn()
    volumes = list(conn.block_storage.volumes())
    return [{"id": v.id, "name": v.name, "size": v.size} for v in volumes]

@app.post("/storage/volumes")
async def create_volume(name: str, size: int, user = Depends(verify_token)):
    conn = get_conn()
    vol = conn.block_storage.create_volume(name=name, size=size)
    print(f"Volume created: {name}")
    return {"id": vol.id, "status": "creating"}

@app.post("/vnf/{server_id}/scale")
async def scale_vnf(server_id: str, flavor: str, user = Depends(verify_token)):
    conn = get_conn()
    server = conn.compute.get_server(server_id)
    flv = conn.compute.find_flavor(flavor)
    print(f"Scaling VNF {server_id} to {flavor}")
    conn.compute.resize_server(server, flv)
    conn.compute.confirm_server_resize(server)
    return {"status": "resizing", "id": server_id}

@app.get("/telemetry/hypervisors")
async def get_hypervisors():
    conn = get_conn()
    hvs = list(conn.compute.hypervisors())
    return [
        {
            "host": hv.hypervisor_hostname,
            "vcpus": hv.vcpus,
            "mem": hv.memory_mb
        } for hv in hvs
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
