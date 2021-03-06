from tornado.testing import AsyncHTTPTestCase
from iot_analytics.server import server
import tornado.escape

class ApiServerTestCase(AsyncHTTPTestCase):

    def get_app(self):
        return server.make_app()

    def test_get(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_post_valid_data(self):
        data = tornado.escape.json_encode({
            'id': 'UA-223344',
            'type': 'event'
        })
        response = self.fetch('/', method="POST", body=data)
        self.assertEqual(response.code, 200)
        self.assertEqual(len(response.body), 0)

    def test_post_no_type(self):
        data = tornado.escape.json_encode({
            'id': 'UA-223344'
        })
        response = self.fetch('/', method="POST", body=data)
        self.assertEqual(response.code, 200)
        self.assertEqual(len(response.body), 0)

    def test_post_no_id(self):
        data = tornado.escape.json_encode({
            'type': 'event'
        })
        response = self.fetch('/', method="POST", body=data)
        self.assertEqual(response.code, 200)
        self.assertEqual(len(response.body), 0)

