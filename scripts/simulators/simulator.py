import requests
import time
import random
from src.common.config import settings

GATEWAY_URL = settings.GATEWAY_URL 
AUTH_URL = f"{GATEWAY_URL}/auth/token"
AMF_URL = f"{GATEWAY_URL}/amf/attach"
NUM_UE = settings.NUM_UE

def get_token(client_id, secret):
    response = requests.post(
        AUTH_URL, 
        data={"username": client_id, "password": secret},
        timeout=5
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Auth failed for {client_id}: {response.status_code}")
        return None

def simulate_ue_flow(ue_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    # Connect amf
    start_t = time.time()
    attach_res = requests.post(AMF_URL, json={"ue_id": ue_id}, headers=headers, timeout=10)
    dur = time.time() - start_t
    if attach_res.status_code == 200:
        data = attach_res.json()
        print(f"UE {ue_id} OK IP: {data.get('assigned_ip')} ({dur:.2f}s)")
    else:
        print(f"UE {ue_id} Fail: {attach_res.status_code}")

def run_simulation():
    # Simulators connect as 'amf-service' for simplicity in this demo identity
    token = get_token("amf-service", "amf-secret")
    if not token:
        print("Error: Can't get token, stopping.")
        return
    print(f"Got token. Sending {NUM_UE} attach requests...")
    for i in range(NUM_UE):
        ue_id = f"imsi-{1000000 + i}"
        simulate_ue_flow(ue_id, token)
        time.sleep(random.uniform(0.1, 0.5))  
    print("Done!")

if __name__ == "__main__":
    run_simulation()
