# gunicorn.conf.py

# -------------------------------------------------
# Server socket
# -------------------------------------------------
bind = "0.0.0.0:8000"

# -------------------------------------------------
# Worker configuration
# -------------------------------------------------
worker_class = "uvicorn.workers.UvicornWorker"

# Good default: (2 x CPU) + 1
workers = 1

# Prevent startup hangs from killing workers
timeout = 120
graceful_timeout = 30

# -------------------------------------------------
# Logging
# -------------------------------------------------
accesslog = "-"
errorlog = "-"
loglevel = "info"

# -------------------------------------------------
# Performance / stability
# -------------------------------------------------
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# -------------------------------------------------
# Preload
# -------------------------------------------------
# DO NOT preload FastAPI apps that touch the DB at import time
preload_app = False
