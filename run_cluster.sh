#!/bin/bash

echo "Starting Mycelium distributed cluster..."

PORT=8000 python -c "from mycelium.runtime.node_rpc import run; run(8000)" &

PORT=8001 python -c "from mycelium.runtime.node_rpc import run; run(8001)" &

PORT=8002 python -c "from mycelium.runtime.node_rpc import run; run(8002)" &
