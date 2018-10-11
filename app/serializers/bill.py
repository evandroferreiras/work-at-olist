from app.core.restplus import api
from flask_restplus import fields

bill_detail = api.model('BillDetailRecord', {
    'destination': fields.String(required=False, description='The phone number receiving the call.', example='51982712345'),
    'start_date': fields.String(required=False, description='Date formated', example='01/11/2018'),
    'start_time': fields.String(required=False, description='Time formated', example='10:30:58'),
    'duration': fields.String(required=False, description='Duration in hour, minute and seconds', example='0h35m42s'),
    'price': fields.String(required=False, description='Price calculated for the call', example='R$ 3,96')
})

bill = api.model('BillRecord', {
    'subscriber': fields.String(required=False, description='The subscriber phone number that originated the call.', example='51982717456'),
    'period': fields.String(required=True, description='the reference period (month/year)', example='02/2017'),
    'records': fields.List(fields.Nested(bill_detail))
})
