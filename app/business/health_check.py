from app.core.db import db


class HealthCheckBus(object):
    def get_status(self):
        is_ok, status = self.health_database_status()
        return {'connected': is_ok, 'status': status}

    def health_database_status(self):
        output = 'connected'
        is_ok = True
        try:
            # to check database we will execute raw query
            session = db.session
            session.execute('SELECT 1')
        except Exception as e:
            output = str(e)
            is_ok = False

        return is_ok, output
