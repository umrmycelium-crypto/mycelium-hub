from mycelium.core.registry_decorator import register
import subprocess
import os

@register("system.status")
def system_status(payload, context):
    """
    Checks the status of core system services.
    """
    # In a real implementation, this would use more robust health checks.
    # For now, we'll check if common ports are listening or if processes are running.
    
    services = {
        "jellyfin": 8096,
        "ollama": 11434,
        "qbittorrent": 8080
    }
    
    results = {}
    for service, port in services.items():
        # Simple check using netstat or ss (requires shell)
        try:
            # Use ss (socket statistics) as it's modern and standard on Fedora
            cmd = f"ss -tuln | grep :{port}"
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            results[service] = "Running" if process.returncode == 0 else "Down"
        except Exception as e:
            results[service] = f"Error: {str(e)}"

    return {
        "status": "OK",
        "services": results
    }


@register("system.deploy")
def system_deploy(payload, context):
    """
    Triggers a system-wide repair and restart.
    """
    script_path = os.path.expanduser("~/mycelium-hub/fix_and_restart.sh")
    
    if not os.path.exists(script_path):
        return {
            "status": "ERROR",
            "message": f"Deployment script not found at {script_path}"
        }

    try:
        # Running the script. Note: This is a destructive/heavy action.
        result = subprocess.run([script_path], capture_output=True, text=True)
        
        return {
            "status": "OK",
            "message": "Repair and restart triggered successfully",
            "output": result.stdout
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Deployment failed: {str(e)}"
        }
