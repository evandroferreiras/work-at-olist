from app.core.restplus import api
from flask_restplus import fields

call = api.model('CallRecord', {
    'id': fields.Integer(readonly=True, description='Record unique identificator', example=10),
    'type': fields.String(required=True, description='Indicate if it''s a call "start" or "end" record', example='start'),
    'timestamp': fields.DateTime(required=True, description='The timestamp of when the event occured', example='2014-01-01T15:00:00Z'),
    'call_id': fields.Integer(required=True, description='Unique for each call record pair', example=10),
    'source': fields.String(required=False, description='The subscriber phone number that originated the call.', example='51982717456'),
    'destination': fields.String(required=False, description='The phone number receiving the call.', example='51982888884')
})
