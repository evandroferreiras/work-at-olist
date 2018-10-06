from flask import Flask, Blueprint
from flask_restplus import Api
from app.core.log_wrapper import log

bp = Blueprint('api', __name__)
api = Api(bp, version='1.0', title='Calls API',
          description='A Olist test', validate=True)


def init_app():
    app = Flask(__name__)
    app.config['ERROR_404_HELP'] = False
    app.register_blueprint(bp)
    return app


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500
