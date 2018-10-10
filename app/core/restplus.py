from flask import Flask, Blueprint
from flask_restplus import Api
from app.core.log_wrapper import log
from app.core.settings import LocalhostConfig, ProductionConfig, TestConfig
from app.core.env_var_wrapper import EnvironmentVariableWrapper
from werkzeug.contrib.fixers import ProxyFix
from jsonschema import FormatChecker

bp = Blueprint('api', __name__)
api = Api(bp, version='1.0', title='Calls API',
          description='A Olist test', validate=True,
          format_checker=FormatChecker(formats=('date-time',)),
          doc='/docs')


def init_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    env = EnvironmentVariableWrapper().env()
    if env == 'development':
        LocalhostConfig(app).config()
    elif env == 'production':
        ProductionConfig(app).config()
    elif env == 'test':
        TestConfig(app).config()
    else:
        raise ValueError(
            'Please, inform FLASK_ENV. Possible values = ' +
            '[development, qa, production]')

    app.register_blueprint(bp)
    return app


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500
