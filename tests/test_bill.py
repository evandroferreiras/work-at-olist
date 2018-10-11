import json
import urllib
from datetime import datetime
from tests.base import BaseTestCase


class BillTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_if_return_filtered_period(self):
        self.setup_data()
        query_string = {
            "subscriber": "51982717456",
            "period": "02/2014"
        }
        rv = self.app.get('/bill?' + urllib.parse.urlencode(query_string))
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual('02/2014', rjson['period'])
        self.assertEqual(1, len(rjson['records']))
        self.assertEqual('51982888925', rjson['records'][0]['destination'])
        self.assertEqual('01/02/2014', rjson['records'][0]['start_date'])
        self.assertEqual('02:00:00', rjson['records'][0]['start_time'])
        self.assertEqual('1:05:00', rjson['records'][0]['duration'])
        self.assertEqual("R$ 97.56", rjson['records'][0]['price'])

    def test_if_return_more_than_one_record(self):
        self.setup_data()
        query_string = {
            "subscriber": "51982717456",
            "period": "01/2014"
        }
        rv = self.app.get('/bill?' + urllib.parse.urlencode(query_string))
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual('01/2014', rjson['period'])
        self.assertEqual(2, len(rjson['records']))
        self.assertEqual('51982881001', rjson['records'][0]['destination'])
        self.assertEqual('01/01/2014', rjson['records'][0]['start_date'])
        self.assertEqual('15:00:00', rjson['records'][0]['start_time'])
        self.assertEqual('0:05:00', rjson['records'][0]['duration'])
        self.assertEqual("R$ 0.81", rjson['records'][0]['price'])
        self.assertEqual('51982881000', rjson['records'][1]['destination'])
        self.assertEqual('30/01/2014', rjson['records'][1]['start_date'])
        self.assertEqual('16:00:00', rjson['records'][1]['start_time'])
        self.assertEqual('0:15:00', rjson['records'][1]['duration'])
        self.assertEqual("R$ 1.71", rjson['records'][1]['price'])

    def test_if_return_last_period_when_not_informed(self):
        self.setup_data()
        rv = self.app.get('/bill?subscriber=51982717456')
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual('03/2014', rjson['period'])
        self.assertEqual(1, len(rjson['records']))
        self.assertEqual('51982888900', rjson['records'][0]['destination'])
        self.assertEqual('01/03/2014', rjson['records'][0]['start_date'])
        self.assertEqual('15:00:00', rjson['records'][0]['start_time'])
        self.assertEqual('0:05:00', rjson['records'][0]['duration'])
        self.assertEqual("R$ 0.81", rjson['records'][0]['price'])

    def test_if_subscriber_argument_is_required(self):
        rv = self.app.get('/bill')
        self.assertEqual(400, rv.status_code)
        self.assertIn('subscriber', rv.json['message'])
        self.assertIn('required', rv.json['message'])

    def test_if_fail_when_informed_period_is_not_closed_yet(self):
        self.setup_data()
        query_string = {
            "subscriber": "51982717456",
            "period": datetime.utcnow().strftime("%m/%Y")
        }
        rv = self.app.get('/bill?' + urllib.parse.urlencode(query_string))
        self.assertEqual(400, rv.status_code)
        self.assertIn('period', rv.json['message'])
        self.assertIn('invalid value', rv.json['message'])

    def test_if_fail_when_subscriber_receive_invalid_value(self):
        rv = self.app.get('/bill?subscriber=invalidvalue')
        self.assertEqual(400, rv.status_code)
        self.assertIn('subscriber', rv.json['message'])
        self.assertIn('invalid value', rv.json['message'])

    def test_if_return_empty_result_when_without_data(self):
        rv = self.app.get('/bill?subscriber=51982717456')
        self.assertEqual('51982717456', rv.json['subscriber'])
        self.assertIsNone(rv.json['period'])
        self.assertEqual([], rv.json['records'])
        self.assertEqual(200, rv.status_code)

    def test_if_duration_is_zero(self):
        self.setup_data()
        query_string = {
            "subscriber": "51982719999",
            "period": "11/2014"
        }
        rv = self.app.get('/bill?' + urllib.parse.urlencode(query_string))
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual('11/2014', rjson['period'])
        self.assertEqual(1, len(rjson['records']))
        self.assertEqual('51982888884', rjson['records'][0]['destination'])
        self.assertEqual('01/11/2014', rjson['records'][0]['start_date'])
        self.assertEqual('15:00:00', rjson['records'][0]['start_time'])
        self.assertEqual('0:00:00', rjson['records'][0]['duration'])
        self.assertEqual("R$ 0.36", rjson['records'][0]['price'])

    def setup_data(self):
        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": "2014-01-01T15:00:00Z",
                          "call_id": 1,
                          "source": "51982717456",
                          "destination": "51982881001"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": "2014-01-01T15:05:00Z",
                          "call_id": 1
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": "2014-01-30T16:00:00Z",
                          "call_id": 2,
                          "source": "51982717456",
                          "destination": "51982881000"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": "2014-01-30T16:15:00Z",
                          "call_id": 2
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": "2014-02-01T02:00:00Z",
                          "call_id": 3,
                          "source": "51982717456",
                          "destination": "51982888925"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": "2014-02-01T03:05:00Z",
                          "call_id": 3
                      }),
                      content_type='application/json')

        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": "2014-03-01T15:00:00Z",
                          "call_id": 4,
                          "source": "51982717456",
                          "destination": "51982888900"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": "2014-03-01T15:05:00Z",
                          "call_id": 4
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "call_id": 5,
                          "source": "51982717456",
                          "destination": "51982888884"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "call_id": 5
                      }),
                      content_type='application/json')

        self.app.post('/call',
                      data=json.dumps({
                          "type": "start",
                          "timestamp": "2014-11-01T15:00:00Z",
                          "call_id": 6,
                          "source": "51982719999",
                          "destination": "51982888884"
                      }),
                      content_type='application/json')
        self.app.post('/call',
                      data=json.dumps({
                          "type": "end",
                          "timestamp": "2014-11-01T15:00:00Z",
                          "call_id": 6
                      }),
                      content_type='application/json')
