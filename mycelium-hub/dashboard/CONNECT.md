# Mycelium Cortex - Multi-Device Connection Guide

## 🌐 Access Points

Your Mycelium cortex is running and accessible from multiple devices on your network.

### Primary Access
- **Local:** `http://127.0.0.1:8082/dashboard/`
- **Local Network:** `http://10.0.0.221:8082/dashboard/`

### Available Services
| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Dashboard | 8082 | HTTP | Visual interface |
| Daemon API | 8000 | HTTP/WS | Data & WebSocket |

## 📱 Device Connection Instructions

### Desktop/Laptop (Same Machine)
```bash
# Already configured - just open:
xdg-open http://127.0.0.1:8082/dashboard/
```

### Other Linux/Mac Machines
```bash
# In terminal, open in default browser:
xdg-open http://10.0.0.221:8082/dashboard/
# OR
open http://10.0.0.221:8082/dashboard/
```

### Windows Machines
1. Open Command Prompt or PowerShell
2. Run: `start http://10.0.0.221:8082/dashboard/`
3. Or simply open your browser and navigate to: `http://10.0.0.221:8082/dashboard/`

### Mobile Devices (Phone/Tablet)
1. Connect to the same WiFi network as this machine
2. Open your mobile browser
3. Navigate to: `http://10.0.0.221:8082/dashboard/`

## 🛡️ Firewall & Network Notes

The servers are configured with:
- **Bind Address:** `0.0.0.0` (accessible from any device on your network)
- **Port 8000:** Daemon WebSocket and REST API
- **Port 8082:** HTTP dashboard server

If you can't connect from another device:
1. Check you're on the same network
2. Verify the IP address: `10.0.0.221`
3. Ensure no firewall is blocking ports 8000 and 8082

## 🤖 Auto-Pilot Status

The system has automatic monitoring:
- **Keep-Alive Script:** `/home/mycelium/mycelium-hub/keep_alive_v2.sh`
- **Checks every:** 15 seconds
- **Auto-restarts:** Both servers if they crash
- **Logs:** `/tmp/mycelium_autopilot.log`

To check status:
```bash
# Check servers are running
ss -tlnp | grep -E "8000|8082"

# Check keep-alive is running
ps aux | grep keep_alive

# View auto-pilot log
tail -f /tmp/mycelium_autopilot.log
```

## 🌱 Growth & Evolution

The system evolves autonomously:
- **Tick rate:** Every 0.2 seconds
- **New ideas:** Generated continuously from node interactions
- **Node dynamics:** Decay, influence, and convergence
- **Intent field:** Emergent from the idea field

### Current State (as of last check)
- Tick: ~12,700+
- Ideas: ~10,400+
- Nodes: seed, memory, intent + converged nodes

## 📚 Documentation & Files

All project files and documentation are available for reference:
- **Core docs:** `/home/mycelium/mycelium-hub/docs/`
- **Evolution history:** `/home/mycelium/mycelium-hub/mycelium-hub/PROJECT_EVOLUTION.md`
- **Runtime:** `/home/mycelium/mycelium-hub/mycelium/`

## 🎯 Quick Start for Any Device

**Just open this URL in any browser:**
```
http://10.0.0.221:8082/dashboard/
```

The visualization will show your live, evolving idea-field with all nodes and connections.
