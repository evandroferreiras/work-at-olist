from datetime import timedelta, datetime


class PriceBus(object):
    def calc_price(self, started_date, finished_date):
        final_price = 0.36

        list_days = self.daterange(started_date, finished_date)

        for start_date, end_date in list_days:
            hour_started = start_date.hour
            hour_finished = end_date.hour
            if hour_started <= 6:
                start_date = datetime(
                    start_date.year, start_date.month, start_date.day, 6, 0, 0)
            if hour_started >= 22:
                start_date = datetime(
                    start_date.year, start_date.month, start_date.day, 0, 0, 0)
            if hour_finished >= 22:
                end_date = datetime(
                    end_date.year, end_date.month, end_date.day, 22, 0, 0)
            if hour_finished <= 6:
                end_date = datetime(
                    end_date.year, end_date.month, end_date.day, 0, 0, 0)

            total_min = int(((end_date - start_date).seconds / 60))
            final_price = final_price + (total_min * 0.09)

        return float("{0:.2f}".format(final_price))

    def daterange(self, start_date, end_date):
        if (end_date - start_date).days > 0:
            result = []
            for n in range(int((end_date - start_date).days + 1)):
                date = datetime(start_date.year, start_date.month,
                                start_date.day) + timedelta(n)
                result.append((date, datetime(date.year,
                                              date.month, date.day, 23, 59, 59)))

            first_day = result[0]
            result[0] = (datetime(first_day[0].year,
                                  first_day[0].month,
                                  first_day[0].day,
                                  start_date.hour,
                                  start_date.minute,
                                  start_date.second),
                         first_day[1])
            last_day = result[len(result) - 1]
            result[len(result) - 1] = (last_day[0],
                                       datetime(last_day[0].year,
                                                last_day[0].month,
                                                last_day[0].day,
                                                end_date.hour,
                                                end_date.minute,
                                                end_date.second))
            return result
        else:
            return [(start_date, end_date)]
