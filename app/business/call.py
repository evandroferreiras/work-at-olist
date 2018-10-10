import re
from datetime import datetime
from app.core.db import db
from app.db_models.call import Call, CallDetail
from sqlalchemy.exc import IntegrityError


REGEX_VALIDATE_PHONE = r'^(\d\d\d\d\d\d\d\d\d\d\d)$'


class CallBus(object):

    def process_call(self, api_payload):
        call_type = api_payload['type'].lower()
        if call_type != 'start' and call_type != 'end':
            raise ValueError('invalid value for field \'type\'.')
        if call_type == 'start':
            if 'source' not in api_payload:
                raise ValueError('required field \'source_phone\' missing')
            if 'destination' not in api_payload:
                raise ValueError('required field \'destination\' missing')
            if not re.match(REGEX_VALIDATE_PHONE, api_payload['source']):
                raise ValueError('invalid value for field \'source\'.')
            if not re.match(REGEX_VALIDATE_PHONE, api_payload['destination']):
                raise ValueError('invalid value for field \'destination\'.')
            id = self.__start_call(
                api_payload['call_id'],
                api_payload['source'],
                api_payload['destination'],
                api_payload['timestamp'])
        elif call_type == 'end':
            id = self.__end_call(
                api_payload['call_id'],
                api_payload['timestamp'])
        api_payload['id'] = id
        return api_payload

    def __start_call(self, call_id, source_phone, destination_phone, date_str):
        try:
            call = Call()
            call.id = call_id
            call.source_phone = source_phone
            call.destination_phone = destination_phone
            db.session.add(call)

            call_detail = CallDetail()
            call_detail.call_id = call_id
            call_detail.date_added = datetime.strptime(
                date_str, '%Y-%m-%dT%H:%M:%SZ')
            call_detail.detail_type_id = 1  # Start
            db.session.add(call_detail)
            db.session.commit()
            return call_detail.id
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError('\'call_id\' has already started.')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def __end_call(self, call_id, date_str):
        try:
            if db.session.query(CallDetail.query.filter(CallDetail.call_id == call_id, CallDetail.detail_type_id == 2).exists()).scalar():
                raise ValueError('\'call_id\' has already ended.')

            if not db.session.query(Call.query.filter(Call.id == call_id).exists()).scalar():
                raise ValueError('invalid value for field \'call_id\'')
            call_detail = CallDetail()
            call_detail.call_id = call_id
            call_detail.date_added = datetime.strptime(
                date_str, '%Y-%m-%dT%H:%M:%SZ')
            call_detail.detail_type_id = 2  # End
            db.session.add(call_detail)
            db.session.commit()
            return call_detail.id
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
