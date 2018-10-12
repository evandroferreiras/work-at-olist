from copy import copy
from tests.base import BaseTestCase
import json


class CallStartTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.post_data = dict(
            type="start",
            timestamp="2014-01-01T15:00:00Z",
            call_id=10,
            source="51982717456",
            destination="51982888884"
        )
        self.return_data = dict(
            type="start",
            timestamp="2014-01-01T15:00:00Z",
            call_id=10,
            source="51982717456",
            destination="51982888884"
        )

    def test_if_save_with_success(self):
        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, rjson['id'])
        for key, value in self.return_data.items():
            self.assertEqual(value, rjson[key])

    def test_if_ignore_changes_after_insert_first_call(self):
        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, rjson['id'])
        for key, value in self.return_data.items():
            self.assertEqual(value, rjson[key])

        post_data = dict(
            type="start",
            timestamp="2014-01-01T15:55:00Z",
            call_id=10,
            source="51982323232",
            destination="51982888884"
        )
        rv = self.app.post('/call', data=json.dumps(post_data),
                           content_type='application/json')
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, rjson['id'])
        for key, value in self.return_data.items():
            self.assertEqual(value, rjson[key])

    def test_if_fail_when_missing_required_fields(self):
        required_fields = [
            'type',
            'timestamp',
            'call_id',
            'source',
            'destination'
        ]
        for value in required_fields:
            post_data = copy(self.post_data)
            post_data.pop(value, None)
            rv = self.app.post('/call', data=json.dumps(post_data),
                               content_type='application/json')
            if 'errors' in rv.json:
                error_msg = list(rv.json['errors'].values())[0]
            else:
                error_msg = rv.json['message']
            self.assertIn('required', error_msg)
            self.assertEqual(400, rv.status_code)

    def test_if_fail_when_field_type_is_invalid(self):
        post_data = copy(self.post_data)
        post_data['type'] = 'wrong value'
        rv = self.app.post(
            '/call', data=json.dumps(post_data), content_type='application/json')
        self.assertIn('message', rv.json)
        message = rv.json['message']
        self.assertEqual(
            "invalid value for field 'type'.", message)
        self.assertEqual(400, rv.status_code)

    def test_if_fail_when_type_is_wrong(self):
        wrong_post_data = dict(
            type=1,
            timestamp="2014-01",
            call_id="teste",
            source=1,
            destination=1
        )
        for key, value in self.post_data.items():
            post_data = copy(self.post_data)
            post_data[key] = wrong_post_data[key]
            rv = self.app.post('/call', data=json.dumps(post_data),
                               content_type='application/json')
            self.assertIn('errors', rv.json)
            errors = rv.json['errors']
            self.assertEqual(key, list(errors.keys())[0])
            self.assertEqual(400, rv.status_code)

    def test_if_is_validating_phone_mask(self):
        wrong_post_data = dict(
            source='55',
            destination='558585'
        )
        for key, value in wrong_post_data.items():
            post_data = copy(self.post_data)
            post_data[key] = wrong_post_data[key]
            rv = self.app.post('/call', data=json.dumps(post_data),
                               content_type='application/json')
            error = rv.json['message']
            self.assertIn(key, error)
            self.assertEqual(400, rv.status_code)


class CallEndTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.post_data = dict(
            type="end",
            timestamp="2014-01-01T15:00:00Z",
            call_id=10
        )
        self.return_data = dict(
            type="end",
            timestamp="2014-01-01T15:00:00Z",
            call_id=10
        )
        self.start_post_data = dict(
            type="start",
            timestamp="2014-01-01T15:00:00Z",
            call_id=10,
            source="51982717456",
            destination="51982888884"
        )

    def test_if_save_with_success(self):
        self.app.post('/call', data=json.dumps(self.start_post_data),
                      content_type='application/json')

        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rjson = rv.json
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, rjson['id'])
        for key, value in self.return_data.items():
            self.assertEqual(value, rjson[key])

    def test_if_save_without_start_call(self):
        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rjson = rv.json
        print(rjson)
        self.assertEqual(200, rv.status_code)
        self.assertEqual(1, rjson['id'])
        for key, value in self.return_data.items():
            self.assertEqual(value, rjson[key])

    def test_if_fail_when_the_call_has_already_ended(self):
        self.app.post('/call', data=json.dumps(self.start_post_data),
                      content_type='application/json')
        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rv = self.app.post('/call', data=json.dumps(self.post_data),
                           content_type='application/json')
        rjson = rv.json
        self.assertEqual(400, rv.status_code)
        self.assertEqual('\'call_id\' has already ended.', rjson['message'])

    def test_if_fail_when_missing_required_fields(self):
        required_fields = [
            'type',
            'timestamp',
            'call_id'
        ]
        for value in required_fields:
            post_data = copy(self.post_data)
            post_data.pop(value, None)
            rv = self.app.post('/call', data=json.dumps(post_data),
                               content_type='application/json')
            if 'errors' in rv.json:
                error_msg = list(rv.json['errors'].values())[0]
            else:
                error_msg = rv.json['message']
            self.assertIn('required', error_msg)
            self.assertEqual(400, rv.status_code)

    def test_if_fail_when_field_type_is_invalid(self):
        post_data = copy(self.post_data)
        post_data['type'] = 'wrong value'
        rv = self.app.post(
            '/call', data=json.dumps(post_data), content_type='application/json')
        self.assertIn('message', rv.json)
        message = rv.json['message']
        self.assertEqual(
            "invalid value for field 'type'.", message)
        self.assertEqual(400, rv.status_code)

    def test_if_fail_when_type_is_wrong(self):
        wrong_post_data = dict(
            type=1,
            timestamp="2014-01",
            call_id="teste",
        )
        for key, value in self.post_data.items():
            post_data = copy(self.post_data)
            post_data[key] = wrong_post_data[key]
            rv = self.app.post('/call', data=json.dumps(post_data),
                               content_type='application/json')
            self.assertIn('errors', rv.json)
            errors = rv.json['errors']
            self.assertEqual(key, list(errors.keys())[0])
            self.assertEqual(400, rv.status_code)
