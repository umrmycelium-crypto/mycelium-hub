#!/bin/bash
uvicorn mycelium.runtime.web_dashboard:app --host 0.0.0.0 --port 8080 --reload
