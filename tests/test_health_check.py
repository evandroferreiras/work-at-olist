from tests.base import BaseTestCase


class HealthCheckTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_health_check_is_success(self):
        rv = self.app.get(
            '/health-check', content_type='application/json')
        rjson = rv.json
        self.assertEqual(rjson['connected'], True)
        self.assertEqual(rjson['status'], 'connected')
        self.assertEqual(200, rv.status_code)

    def test_health_check_when_db_is_offline(self):
        super().setUp('invalid_connection_string')
        rv = self.app.get(
            '/health-check', content_type='application/json')
        rjson = rv.json
        self.assertEqual(rjson['connected'], False)
        self.assertEqual(
            rjson['status'], "Could not parse rfc1738 URL from string 'invalid_connection_string'")
        self.assertEqual(200, rv.status_code)
