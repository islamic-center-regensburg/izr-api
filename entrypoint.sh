#!/bin/sh
set -e
service ssh start
exec .venv/bin/python -m gunicorn src.main:app
# exec .venv/bin/python -m uvicorn src.main:app --proxy-headers --host 0.0.0.0 --port 8000
