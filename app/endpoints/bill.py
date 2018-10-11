from flask import abort
from app.core.restplus import api
from app.serializers.bill import bill
from app.business.bill import BillBus
from app.parsers.bill import bill_get_parser

from flask_restplus import Resource

ns_default = api.default_namespace


@ns_default.route('/bill')
class BillView(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, args, kwargs)

    @ns_default.expect(bill_get_parser)
    @ns_default.marshal_with(bill)
    def get(self):
        try:
            args = bill_get_parser.parse_args()
            bill = BillBus()
            return bill.get_bill(args)
        except Exception as e:
            abort(400, str(e))
