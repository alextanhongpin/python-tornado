import tornado
import tornado.ioloop
import tornado.web
import tornado.autoreload
import os

import service.echo as echo

port = 8888

class MainHandler(tornado.web.RequestHandler):
    service = echo.make_service()
    def get(self):
        res = self.service.echo('')
        self.write(', '.join(res))
                                                                                                                                                                          # $ curl -XPOST -H 'Content-Type: application/json' -d '{"msg": "something else"}' http://localhost:8888/
    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        res = self.service.echo(req['msg'])
        self.write(', '.join(res))

def make_app():
    return tornado.web.Application([
            (r'/', MainHandler)
        ])

if __name__ == '__main__':
    app = make_app()
    app.listen(port)
    print(f'listening to port*:{port}. press ctrl + c to cancel')

    # TODO: Enable only in development mode.
    tornado.autoreload.start()
    for dir, _, files in os.walk('service'):
        [tornado.autoreload.watch(f'dir/{f}')
                for f in files if not f.startswith('.')]

    tornado.ioloop.IOLoop.current().start()
