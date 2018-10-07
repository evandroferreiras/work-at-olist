
from app.core.resources import init_resources
from app.core.restplus import init_app
from app.core.db import init_db
from app.core.log_wrapper import init_log, log

init_log()
init_resources()

app = init_app()
init_db(app)
log.info('Service started')
