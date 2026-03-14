import subprocess
import time

def scale_deployment(deployment_name: str, replicas: int):
    print(f"Scaling deployment {deployment_name} to {replicas} replicas")
    cmd = [
        "kubectl",
        "scale",
        "deployment",
        deployment_name,
        f"--replicas={replicas}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Deployment scaled successfully")
    else:
        print("Failed to scale deployment")
        print(result.stderr)

def restart_pod(pod_name: str):
    print(f"Restarting pod {pod_name}")
    cmd = ["kubectl", "delete", "pod", pod_name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Pod deleted. Kubernetes will recreate it")
    else:
        print("Failed to restart pod")
        print(result.stderr)

def check_system_health():
    print("Checking system health")
    return True

def monitor_loop():
    deployment = "example-deployment"
    while True:
        healthy = check_system_health()
        if not healthy:
            print("System unhealthy")
            scale_deployment(deployment, 3)
        time.sleep(60)

if __name__ == "__main__":
    monitor_loop()