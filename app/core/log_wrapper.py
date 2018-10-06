import logging
import sys

log = logging.getLogger('flask')


def init_log():
    log_werkzeug = logging.getLogger('werkzeug')
    log_werkzeug.handlers = []
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s] requested %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    log.handlers = []
    log.addHandler(handler)
