from tornado_cors import CorsMixin
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado import escape
from iot_analytics.models import get_model_for_type


class MainHandler(CorsMixin, RequestHandler):

    def initialize(self, database):
        self.database = database

    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write({})

    def post(self):
        import urlparse

        content_type = self.request.headers.get('Content-Type')

        if 'form-urlencoded' in content_type:
            parsed = urlparse.parse_qs(self.request.body)
            data = {}

            # Normalize the urldecoded data
            for p in parsed:
                data[p] = parsed[p][0]
        else:
            data = escape.json_decode(self.request.body)

        if "type" in data:
            tracking_id = data.pop("id", None)
            event_type = data.pop("type", None)

            Obj = get_model_for_type(event_type)
            obj = Obj(tracking_id, data)

            if obj.is_valid():
                self.database.add(obj)

def make_database():
    from iot_analytics.interfaces import FileStorageInterface
    return FileStorageInterface()

def make_app():
    return Application([
       (r"/", MainHandler, dict(database=make_database())),
    ])

if __name__ == "__main__":
    application = make_app()
    application.listen(4000)
    IOLoop.instance().start()
