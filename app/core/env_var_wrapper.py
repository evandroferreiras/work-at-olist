import os


class EnvironmentVariableWrapper(object):
    def __get_env_value(self, key):
        value = os.environ.get(key)
        if value:
            return value
        else:
            raise ValueError('We cant find value of env.variable:' + key)

    def localhost_database_uri(self):
        return self.__get_env_value('LOCALHOST_DATABASE_URI')

    def prod_database_uri(self):
        return self.__get_env_value('PROD_DATABASE_URI')

    def env(self):
        return self.__get_env_value('FLASK_ENV')
