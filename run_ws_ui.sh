#!/bin/bash
uvicorn mycelium.runtime.ws_dashboard:app --host 0.0.0.0 --port 8090 --reload
