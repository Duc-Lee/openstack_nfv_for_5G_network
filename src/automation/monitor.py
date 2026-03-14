from src.common.config import settings
import requests
import time
PROMETHEUS_URL = settings.PROMETHEUS_URL

def get_metric(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    results = response.json()['data']['result']
    if results:
        return float(results[0]['value'][1])
    return 0

def monitor_system():
    while True:
        amf_load = get_metric('amf_requests_total')
        smf_sessions = get_metric('smf_sessions_total')
        print(f"Stats: AMF load {amf_load}, SMF sessions {smf_sessions}")
        if amf_load > 100: 
            print("Warning: High load!")
        time.sleep(10)

if __name__ == "__main__":
    monitor_system()
