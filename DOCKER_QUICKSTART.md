# 🚀 Quick Start - Unified Docker Stack

## 30-Second Setup

```bash
cd mycelium-hub
cp .env.production .env

# Edit .env and change passwords:
nano .env

# Start the entire stack
docker-compose -f docker-compose-unified.yml up -d

# Wait 2-5 minutes for all services to start
docker-compose -f docker-compose-unified.yml ps

# Access dashboard
open http://localhost:8082
```

## What's Running?

✅ **Mycelium Hub** (8082) - Intent-driven dashboard  
✅ **Ollama** (11434) - Local LLM (qwen2.5-coder)  
✅ **Rule Engine** (8080) - Vision & rules  
✅ **Jellyfin** (8096) - Media server  
✅ **Radarr** (7878) - Movie manager  
✅ **Sonarr** (8989) - TV manager  
✅ **Jellyseerr** (5055) - Requests  
✅ **qBittorrent** (6880) - Torrents  
✅ **WordPress** (8081) - CMS  
✅ **Baserow** (3000) - Database UI  
✅ **Milvus** (19530) - Vector DB  
✅ **Elasticsearch** (9200) - Search  
✅ **MongoDB** (27017) - Documents  
✅ **PostgreSQL** (5432 + 5433) - Databases  
✅ **Redis** (6379 + 6380) - Caching  
✅ **+6 more services**

## Key Commands

```bash
# View all services
docker-compose -f docker-compose-unified.yml ps

# View logs
docker-compose -f docker-compose-unified.yml logs -f mycelium-hub

# Stop all
docker-compose -f docker-compose-unified.yml down

# Stop & remove volumes (WARNING: data loss)
docker-compose -f docker-compose-unified.yml down -v

# Restart specific service
docker-compose -f docker-compose-unified.yml restart mycelium-hub

# Execute command in container
docker-compose -f docker-compose-unified.yml exec mycelium-hub bash

# View resource usage
docker stats
```

## Default Ports

```
8000  - Mycelium API
8082  - Mycelium Dashboard
8080  - Rule Engine
8096  - Jellyfin
8089  - Sonarr
7878  - Radarr
5055  - Jellyseerr
6881  - qBittorrent (Torrent)
8081  - WordPress
3000  - Baserow
3001  - Spore Scribe (MCP)
3002  - The Forge (MCP)
3004  - The Gateway (MCP)
5432  - PostgreSQL (Forged Intent)
5433  - PostgreSQL (Central)
6379  - Redis (Forged Intent)
6380  - Redis (Central)
9000  - Minio API
9001  - Minio Console
9091  - Milvus Admin
9200  - Elasticsearch
19530 - Milvus
27017 - MongoDB
2379  - etcd
1025  - MailHog SMTP
8025  - MailHog UI
```

## Network Communication

All services on `mycelium-net`:

```
mycelium-hub ←→ ollama
           ←→ rule-engine
           ←→ postgres-central
           ←→ milvus-standalone
           ←→ elasticsearch
           ←→ mongodb
           ←→ [all other services]
```

## Emergency Stop

```bash
# Kill all containers
docker-compose -f docker-compose-unified.yml down

# Force remove all
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
```

## Need Help?

- Check logs: `docker-compose -f docker-compose-unified.yml logs <service>`
- Health status: `docker-compose -f docker-compose-unified.yml ps`
- Full guide: See [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)
