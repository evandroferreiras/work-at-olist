from app.core.restplus import api
from app.endpoints.health_check import HealthCheckView


def init_resources():
    api.add_resource(HealthCheckView)
