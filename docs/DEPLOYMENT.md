# 🚀 Deployment & Configuration Guide

## Environment Variables

Mycelium Hub uses environment variables for runtime configuration, especially for LLM backends.

### Configuration Variables

| Variable | Default | Purpose | Required |
|----------|---------|---------|----------|
| `MYCELIUM_OLLAMA_MODEL` | `qwen2.5-coder:latest` | Model for LLM inference (intent synthesis, explanations) | No (uses default if not set) |

### Setting Environment Variables

**Method 1: .env File (Recommended for Local Development)**
```bash
# Copy template
cp .env.example .env

# Edit with your settings
# File is automatically loaded at application startup
```

**Method 2: Export Before Running**
```bash
export MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest
python app.py
```

**Method 3: Inline with Command**
```bash
MYCELIUM_OLLAMA_MODEL=llama2 python app.py
```

**Method 4: Docker Environment**
```yaml
services:
  mycelium:
    environment:
      - MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest
```

**Method 5: Systemd Service**
```ini
[Service]
Environment="MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest"
```

## LLM Model Selection

### Recommended Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| `qwen2.5-coder:latest` | 4.7GB | Medium | Code explanations (default) |
| `llama2` | 3.8GB | Fast | General purpose |
| `mistral` | 4.0GB | Fast | Fast inference |

### Installing Models

```bash
# Pull model from Ollama
ollama pull qwen2.5-coder:latest

# Verify installation
ollama list

# Use it
export MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest
python app.py
```

---

## Deployment State (Forged-Intent Host)

Current services running on: **forged-intent**

| Service | Status | Port |
|---------|--------|------|
| Jellyfin | Running | 8096 |
| Radarr | Running | 7878 |
| Sonarr | Running | 8989 |
| Jellyseerr | Running | 5055 |
| qbittorrent | Running | 8080 (Web), 6881 (Torrent) |

---

## Quick Reference

**For local development:**
```bash
cp .env.example .env
# Edit .env if needed
python app.py
```

**For Docker:**
```bash
docker-compose up -e MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest
```

**For Systemd service:**
```bash
sudo systemctl set-environment MYCELIUM_OLLAMA_MODEL=qwen2.5-coder:latest
sudo systemctl start mycelium-hub
```

See [QUICK_START.md](../QUICK_START.md) for more information.
