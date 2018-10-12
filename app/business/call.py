import re
from datetime import datetime
from app.core.db import db
from app.core.constants import REGEX_VALIDATE_PHONE
from app.business.price import PriceBus
from app.db_models.call import Call


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
            return self.__start_call(
                api_payload['call_id'],
                api_payload['source'],
                api_payload['destination'],
                api_payload['timestamp'])
        elif call_type == 'end':
            return self.__end_call(
                api_payload['call_id'],
                api_payload['timestamp'])
        return None

    def __start_call(self, call_id, source_phone, destination_phone, date_str):
        try:
            call = self.__create_or_get_call(call_id)
            if not call.started_date:
                call.started_date = datetime.strptime(
                    date_str, '%Y-%m-%dT%H:%M:%SZ')
            call = self.__calculate_price(call)

            # If the call not exists yet
            if not call.id:
                call.call_identifier = call_id
                call.source_phone = source_phone
                call.destination_phone = destination_phone
                db.session.add(call)
            db.session.commit()

            return {
                'id': call.id,
                'type': 'start',
                'timestamp': call.started_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'call_id': call.call_identifier,
                'source': call.source_phone,
                'destination': call.destination_phone
            }
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def __end_call(self, call_id, date_str):
        try:
            if db.session.query(Call.query.filter(Call.call_identifier == call_id, Call.finished_date != None).exists()).scalar():  # noqa: E711
                raise ValueError('\'call_id\' has already ended.')
            call = self.__create_or_get_call(call_id)
            if not call.finished_date:
                call.finished_date = datetime.strptime(
                    date_str, '%Y-%m-%dT%H:%M:%SZ')
            call = self.__calculate_price(call)

            # If the call not exists yet
            if not call.id:
                call.call_identifier = call_id
                db.session.add(call)
            db.session.commit()
            return {
                'id': call.id,
                'type': 'end',
                'timestamp': call.finished_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'call_id': call.call_identifier
            }
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    def __create_or_get_call(self, call_id):
        if db.session.query(Call.query.filter(Call.call_identifier == call_id).exists()).scalar():
            call = db.session.query(Call).filter_by(
                call_identifier=call_id).first()
        else:
            call = Call()
        return call

    def __calculate_price(self, call):
        if call.started_date is not None \
                and call.finished_date is not None \
                and call.price is None:
            call.price = PriceBus().calc_price(call.started_date, call.finished_date)
        return call
