# 🚀 Unified Mycelium Docker Stack - Deployment Guide

## Overview

This is a **comprehensive, production-ready Docker Compose stack** that integrates:

- **🧠 Mycelium Hub** - Intent-driven core with LLM (qwen2.5-coder via Ollama)
- **🎯 Forged Intent** - Rule Engine + Vision Pipeline (PostgreSQL + Redis)
- **🔍 Production Memory** - Vector DB (Milvus) + Search (Elasticsearch) + Documents (MongoDB)
- **🌐 MCP Servers** - Knowledge integration (The Gateway, The Forge, Spore Scribe)
- **📰 Studio Stack** - CMS (WordPress) + Database (Baserow)
- **📺 Media Services** - Jellyfin, Radarr, Sonarr, Jellyseerr, qBittorrent

**Total Services**: 30+  
**Network**: Single `mycelium-net` bridge for cross-service communication  
**Storage**: 13 volumes for data persistence  

## ⚡ Quick Start

### 1. Setup Environment

```bash
cd mycelium-hub

# Copy and edit production environment
cp .env.production .env

# Generate strong passwords (Linux/Mac)
openssl rand -base64 32  # Run 4 times and paste into .env

# Or on Windows/PowerShell
[Convert]::ToBase64String((1..32|%{[byte](Get-Random -Max 256)}))
```

### 2. Build & Start

```bash
# Build Docker images
docker-compose -f docker-compose-unified.yml build

# Start all services
docker-compose -f docker-compose-unified.yml up -d

# Watch startup logs
docker-compose -f docker-compose-unified.yml logs -f

# Check service health
docker-compose -f docker-compose-unified.yml ps
```

### 3. Initial Setup

```bash
# Wait for all services to be healthy (~2-5 minutes)
docker-compose -f docker-compose-unified.yml ps

# Test Mycelium Hub
curl http://localhost:8000/status

# Access Dashboard
open http://localhost:8082
```

## 📊 Service Access Points

| Service | URL | Port | Purpose |
|---------|-----|------|---------|
| **Mycelium Hub Dashboard** | http://localhost:8082 | 8082 | Intent-driven UI |
| **Mycelium API** | http://localhost:8000 | 8000 | REST API |
| **Rule Engine** | http://localhost:8080 | 8080 | Vision + Rules |
| **Jellyfin** | http://localhost:8096 | 8096 | Media Server |
| **Radarr** | http://localhost:7878 | 7878 | Movie Manager |
| **Sonarr** | http://localhost:8989 | 8989 | TV Manager |
| **Jellyseerr** | http://localhost:5055 | 5055 | Requests |
| **qBittorrent** | http://localhost:6880 | 6880 | Torrent Client |
| **WordPress** | http://localhost:8081 | 8081 | CMS |
| **Baserow** | http://localhost:3000 | 3000 | Database/CMS |
| **Minio Console** | http://localhost:9001 | 9001 | S3 Storage UI |
| **Elasticsearch** | http://localhost:9200 | 9200 | Search API |
| **Milvus** | http://localhost:19530 | 19530 | Vector DB |
| **MongoDB** | http://localhost:27017 | 27017 | Document DB |
| **MailHog** | http://localhost:8025 | 8025 | Email Testing |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           UNIFIED MYCELIUM DOCKER NETWORK                    │
│                   (mycelium-net)                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🧠 MYCELIUM HUB (Core)                               │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ - Intent Compiler + Router                           │   │
│  │ - LLM Backend (Ollama + qwen2.5-coder)              │   │
│  │ - Event Store + Intent Memory                        │   │
│  │ - Dashboard (8082)                                   │   │
│  └──────────────────────────────────────────────────────┘   │
│               ↓ connects to ↓                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 🎯 FORGED INTENT          🔍 MEMORY LAYER             │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ - Rule Engine (8080)      - Milvus Vector DB         │   │
│  │ - PostgreSQL (5432)       - Elasticsearch (9200)     │   │
│  │ - Redis (6379)            - MongoDB (27017)          │   │
│  │ - Vision Pipeline          - MCP Servers             │   │
│  └──────────────────────────────────────────────────────┘   │
│                       ↓ connects to ↓                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 📰 STUDIO STACK          📺 MEDIA SERVICES            │   │
│  ├──────────────────────────────────────────────────────┤   │
│  │ - WordPress (8081)       - Jellyfin (8096)          │   │
│  │ - Baserow (3000)         - Radarr (7878)            │   │
│  │ - MySQL (3306)           - Sonarr (8989)            │   │
│  │                          - Jellyseerr (5055)         │   │
│  │                          - qBittorrent (6880)        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  🔧 UTILITIES: Watchtower (auto-updates), MailHog (email)   │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Storage: 13 named volumes for persistence
Network: mycelium-net (bridge driver)
```

## 🔐 Security Best Practices

### 1. Change All Passwords

Edit `.env` before starting:

```bash
# Generate secure passwords
POSTGRES_PASSWORD=<strong-random-password>
POSTGRES_CENTRAL_PASSWORD=<strong-random-password>
MINIO_PASSWORD=<strong-random-password>
MONGODB_PASSWORD=<strong-random-password>
WORDPRESS_DB_ROOT_PASSWORD=<strong-random-password>
WORDPRESS_DB_PASSWORD=<strong-random-password>
```

### 2. Network Isolation

```bash
# All services on mycelium-net bridge
# No services exposed to host network except defined ports
# Use firewall rules to restrict access:

# Example: Allow only internal traffic
sudo ufw allow from 172.17.0.0/16 to any
```

### 3. Volume Permissions

```bash
# Set restrictive permissions on mounted data
sudo chown -R 1000:1000 /mnt/media
sudo chmod 755 /mnt/media
```

### 4. Backup Strategy

```bash
# Daily backup of critical volumes
docker run --rm \
  -v postgres_central_data:/source \
  -v /backups:/dest \
  alpine tar czf /dest/postgres-$(date +%Y%m%d).tar.gz -C /source .

# Use `watchtower` for auto-updates (already in stack)
```

## 📈 Monitoring & Troubleshooting

### View Logs

```bash
# All services
docker-compose -f docker-compose-unified.yml logs

# Specific service
docker-compose -f docker-compose-unified.yml logs mycelium-hub

# Follow in real-time
docker-compose -f docker-compose-unified.yml logs -f mycelium-hub
```

### Health Checks

```bash
# All services
docker-compose -f docker-compose-unified.yml ps

# Check specific service
docker exec mycelium-hub-core curl http://localhost:8000/status

# Test MCP server
curl http://localhost:3004/health
```

### Common Issues

**"Port already in use"**
```bash
# Check what's using the port
lsof -i :8082
# Kill the process or change port in docker-compose.yml
```

**"Service fails to start"**
```bash
# Check logs
docker-compose -f docker-compose-unified.yml logs <service-name>

# Restart service
docker-compose -f docker-compose-unified.yml restart <service-name>
```

**"Volume permission denied"**
```bash
# Fix ownership
docker exec <container> chown -R 1000:1000 /config

# Or recreate volume
docker volume rm <volume-name>
```

## 🛠️ Maintenance

### Update Services

```bash
# Pull latest images
docker-compose -f docker-compose-unified.yml pull

# Rebuild and restart
docker-compose -f docker-compose-unified.yml up -d --build
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove unused images
docker image prune -a
```

### Database Backup

```bash
# PostgreSQL
docker exec postgres-central pg_dump -U admin mycelium > backup.sql

# MongoDB
docker exec memsys-mongodb mongodump --out=/backups
```

## 🧵 Service Dependencies

```
Mycelium Hub depends on:
  ├─ Ollama (LLM)
  ├─ PostgreSQL Central (Central DB)
  ├─ Redis Central (Cache)
  ├─ Milvus (Vector DB)
  ├─ Elasticsearch (Search)
  └─ MongoDB (Documents)

Forged Intent depends on:
  ├─ PostgreSQL Forged (Vision DB)
  └─ Redis Forged (Cache)

MCP Servers depend on:
  ├─ Milvus
  ├─ MongoDB
  ├─ Elasticsearch
  └─ Redis Central

Media Services depend on:
  └─ qBittorrent (for downloads)

Baserow depends on:
  ├─ PostgreSQL Central
  └─ Redis Central
```

## 📝 Configuration Examples

### Use Different LLM Model

```bash
# In .env
MYCELIUM_OLLAMA_MODEL=llama2

# Restart
docker-compose -f docker-compose-unified.yml restart mycelium-hub
```

### Enable GPU for Ollama

```bash
# In docker-compose-unified.yml, change:
OLLAMA_NUM_GPU: 1  # from 0

# Requires NVIDIA Docker runtime
docker-compose -f docker-compose-unified.yml up -d ollama
```

### Mount Custom Media Directory

```bash
# Edit volumes section in docker-compose-unified.yml:
volumes:
  - /custom/media/path:/media:ro
```

### Custom Network Configuration

```bash
# Use host network (not recommended for security)
# In service definition, add:
network_mode: "host"
```

## 🚀 Production Deployment

### On Linux Server

```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone https://github.com/umrmycelium-crypto/mycelium-hub.git
cd mycelium-hub

# Setup production environment
cp .env.production .env
# Edit .env with your passwords

# Create systemd service
sudo tee /etc/systemd/system/mycelium-docker.service > /dev/null <<EOF
[Unit]
Description=Mycelium Hub Docker Stack
After=docker.service
Requires=docker.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/mycelium-hub
ExecStart=/usr/local/bin/docker-compose -f docker-compose-unified.yml up
ExecStop=/usr/local/bin/docker-compose -f docker-compose-unified.yml down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable mycelium-docker
sudo systemctl start mycelium-docker

# Monitor
sudo systemctl status mycelium-docker
sudo journalctl -u mycelium-docker -f
```

### On Docker Swarm

```bash
# Initialize swarm (if not already)
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose-unified.yml mycelium
```

### On Kubernetes

```bash
# Convert docker-compose to Kubernetes manifests
kompose convert -f docker-compose-unified.yml -o k8s/

# Deploy
kubectl apply -f k8s/
```

## 📞 Support & Documentation

- **Architecture**: See [ARCHITECTURE.md](../ARCHITECTURE.md)
- **Mycelium Hub**: See [QUICK_START.md](../QUICK_START.md)
- **Individual Services**:
  - [Jellyfin Docs](https://jellyfin.org/docs/)
  - [Radarr Docs](https://radarr.video/)
  - [Sonarr Docs](https://sonarr.tv/)
  - [Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/)
  - [MongoDB Docs](https://docs.mongodb.com/)

**Last Updated**: July 22, 2026  
**Version**: 1.1.0 (Unified Mesh)  
**Status**: ✅ Production Ready  

