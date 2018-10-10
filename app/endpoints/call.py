from flask import abort
from app.core.restplus import api
from app.serializers.call import call
from app.business.call import CallBus
from flask_restplus import Resource

ns_default = api.default_namespace


@ns_default.route('/call')
class CallView(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, args, kwargs)

    @ns_default.expect(call)
    def post(self):
        call = CallBus()
        try:
            return call.process_call(api.payload)
        except Exception as e:
            abort(400, str(e))
