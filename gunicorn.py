"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ


def max_workers():
    return cpu_count()


bind = '0.0.0.0:5000'
backlog = 2048
workers = 2*max_workers()+1
worker_connections = 1000
timeout = 30
keepalive = 2
