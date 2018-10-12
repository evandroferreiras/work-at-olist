import re
import calendar
from datetime import datetime
from monthdelta import monthdelta
from app.core.constants import REGEX_VALIDATE_PHONE
from app.core.db import db
from app.db_models.call import Call


class BillBus(object):
    def get_bill(self, args):
        if not args.get('subscriber'):
            raise ValueError('the argument \'subscriber\' is required.')
        if not re.match(REGEX_VALIDATE_PHONE, args.get('subscriber')):
            raise ValueError('invalid value for argument \'subscriber\'.')

        subscriber = args.get('subscriber')
        period = args.get('period')
        if not period:
            period = self.__get_period(subscriber)
        else:
            dt_period = datetime.strptime(period, '%m/%Y')
            current_period = datetime(
                datetime.utcnow().year, datetime.utcnow().month, 1)
            if dt_period >= current_period:
                raise ValueError(
                    ' invalid value for argument \'period\'. The period must be closed.')

        return {
            'subscriber': subscriber,
            'period': period,
            'records': self.__get_records(subscriber, period)
        }

    def __get_records(self, subscriber, period):
        if not period:
            return []
        dt_period = datetime.strptime(period, '%m/%Y')
        _, last_day = calendar.monthrange(
            dt_period.year, dt_period.month)
        dt_first_day = datetime(dt_period.year, dt_period.month, 1)
        dt_last_day = datetime(dt_period.year, dt_period.month, last_day)
        records = (db.session.query(Call.destination_phone, Call.started_date,
                                    Call.finished_date, Call.price).filter(Call.source_phone == subscriber,
                                                                           Call.finished_date >= dt_first_day,
                                                                           Call.finished_date <= dt_last_day))

        results = []
        for r in records:
            st_date = r.started_date
            fi_date = r.finished_date
            results.append({
                'destination': r.destination_phone,
                'start_date': st_date.strftime('%d/%m/%Y'),
                'start_time': st_date.strftime('%H:%M:%S'),
                'duration': self.__format_duration(st_date, fi_date),
                'price': "R$ " + str(r.price if r.price else 0.00)
            })
        return results

    def __format_duration(self, st_date, fi_date):
        duration = (fi_date - st_date)
        seconds = duration.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f'{"{:.0f}".format(hours)}h{"{:0>2d}".format(minutes)}m{"{:0>2d}".format(seconds)}s'

    def __get_period(self, subscriber):
        last_month = datetime.utcnow() - monthdelta(1)
        last_date = (db.session.query(Call.finished_date)
                     .filter(Call.finished_date <= last_month)
                     .filter(Call.source_phone == subscriber)
                     .order_by(Call.finished_date.desc()).first())
        if last_date:
            last_date = last_date[0]
            return last_date.strftime('%m/%Y')
        else:
            return None
