from app.core.restplus import api
from app.endpoints.health_check import HealthCheckView
from app.endpoints.call import CallView
from app.endpoints.bill import BillView


def init_resources():
    api.add_resource(HealthCheckView)
    api.add_resource(CallView)
    api.add_resource(BillView)
