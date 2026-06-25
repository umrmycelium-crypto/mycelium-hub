#!/bin/bash

echo "Stopping uvicorn processes..."
pkill -f uvicorn || true
pkill -f dashboard_server || true

echo "Checking ports..."
ss -tulpn | grep -E '8080|8081' || echo "No dashboard ports in use"
