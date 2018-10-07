from app.core.env_var_wrapper import EnvironmentVariableWrapper


class BaseConfig(object):
    def __init__(self, app):
        self.app = app
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['ERROR_404_HELP'] = False


class LocalhostConfig(BaseConfig):
    def config(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = EnvironmentVariableWrapper(
        ).localhost_database_uri()


class ProductionConfig(BaseConfig):
    def config(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = EnvironmentVariableWrapper(
        ).prod_database_uri()


class TestConfig(BaseConfig):
    def config(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
