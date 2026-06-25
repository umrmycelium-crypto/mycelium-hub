#!/bin/bash

python -c "from mycelium.runtime.node_mesh import register_node; register_node('http://localhost:8000')"
python -c "from mycelium.runtime.node_mesh import register_node; register_node('http://localhost:8001')"
python -c "from mycelium.runtime.node_mesh import register_node; register_node('http://localhost:8002')"
