# Gunicorn Configuration for Django HTTPS Deployment
# This configuration file sets up Gunicorn as a WSGI server for production

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"  # Bind to localhost on port 8000
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal number of workers
worker_class = "sync"  # Use sync workers for Django
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/gunicorn/django_access.log"
errorlog = "/var/log/gunicorn/django_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "django_library_app"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/django.pid"
user = "www-data"  # Change to your web server user
group = "www-data"  # Change to your web server group
tmp_upload_dir = None

# SSL Configuration (if running Gunicorn with SSL directly)
# keyfile = "/path/to/your/private.key"
# certfile = "/path/to/your/certificate.crt"

# Security settings
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Preload application for better performance
preload_app = True

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=LibraryProject.settings',
    'PYTHONPATH=/path/to/your/project',  # Update with your project path
]

# Worker timeout
worker_tmp_dir = "/dev/shm"  # Use shared memory for better performance

# Graceful timeout
graceful_timeout = 30

# Security headers (handled by reverse proxy, but can be set here too)
def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Django Library Management System is ready to serve requests")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")

# SSL/TLS Configuration for direct HTTPS serving (alternative to reverse proxy)
# Uncomment and configure if you want Gunicorn to handle SSL directly
# keyfile = "/path/to/your/ssl/private.key"
# certfile = "/path/to/your/ssl/certificate.crt"
# ssl_version = "TLSv1.2"
# ciphers = "ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384"
