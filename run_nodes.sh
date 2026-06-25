#!/bin/bash

export MYCELIUM_NODE_ID=node-1
python -m mycelium.runtime.node &

export MYCELIUM_NODE_ID=node-2
python -m mycelium.runtime.node &

export MYCELIUM_NODE_ID=node-3
python -m mycelium.runtime.node &
