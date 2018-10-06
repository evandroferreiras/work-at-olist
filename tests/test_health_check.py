from tests.base import BaseTestCase


class HealthCheckTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_health_check_is_sucess(self):
        rv = self.app.get(
            '/health-check', content_type='application/json')
        rjson = rv.json
        self.assertEqual(rjson['message'], 'its working')
        self.assertEqual(200, rv.status_code)
