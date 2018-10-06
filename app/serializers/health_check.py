from app.core.restplus import api
from flask_restplus import fields

health_check_serializer = api.model('HealthCheck', {
    'message': fields.String(readonly=True, description='The status message', example='its working')
})
