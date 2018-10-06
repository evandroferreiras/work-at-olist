from app.core.restplus import api
from app.business.health_check import HealthCheckBus
from app.serializers.health_check import health_check_serializer
from flask_restplus import Resource

ns_default = api.default_namespace


@ns_default.route('/health-check')
class HealthCheckView(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, args, kwargs)
        self.health_check_bus = HealthCheckBus()

    @ns_default.marshal_with(health_check_serializer)
    def get(self):
        return self.health_check_bus.get_status()
