#!/bin/sh
cd "$(dirname "$0")"
exec .venv/bin/python -m uvicorn soilquest.api:app --host 127.0.0.1 --port 8104
