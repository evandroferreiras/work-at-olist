from app.core.restplus import api
from flask_restplus import fields

health_check_serializer = api.model('HealthCheck', {
    'connected': fields.Boolean(readonly=True, description='True if is database connected', example=True),
    'status': fields.String(readonly=True, description='The database status', example='Some error ')
})
