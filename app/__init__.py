
from app.core.resources import init_resources
from app.core.restplus import init_app
from app.core.log_wrapper import init_log, log

init_log()
init_resources()

app = init_app()
log.info('Service started')
