from functools import partial
import os
import signal
import time
import logging

import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging
enable_pretty_logging()

#  import mysql.connector
import pymysql

import service.echo as echo

port = 8888
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, service: echo.interface.Service):
        self.service = service

    def get(self):
        res = self.service.echo('')
        self.write(', '.join(res))
                                                                                                                                                                          # $ curl -XPOST -H 'Content-Type: application/json' -d '{"msg": "something else"}' http://localhost:8888/
    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        res = self.service.echo(req['msg'])
        self.write(', '.join(res))


def test_db():
    host = os.getenv('DB_HOST', '127.0.0.1')
    user = os.getenv('DB_USER', 'john')
    password = os.getenv('DB_PASS', '123456')
    database = os.getenv('DB_NAME', 'python_test')

    #  http://zetcode.com/python/pymysql/
    try:
        con = pymysql.connect(host, user, password, database)
    except pymysql.err.OperationalError as err:
        #  https://github.com/PyMySQL/PyMySQL/blob/master/pymysql/err.py
        print('got error', err)
        raise err
    except Exception as e:
        print('handle unknown exception', e)

    with con:
        cur = con.cursor()
        cur.execute('select 1 + 1')
        result = cur.fetchone()
        print(f'result is {result}')
    #  except mysql.connector.Error as err:
       #  print(err)

    print('mysql closed')

def sig_handler(server, sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    async def shutdown():
        logging.info('stopping the server')
        server.stop()
        logging.info('will shutdown in %s seconds', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        await tornado.gen.sleep(MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        io_loop.stop()

    logging.warning('caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)

if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler, dict(service=echo.make_service()))
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)
    print(f'listening to port*:{port}. press ctrl + c to cancel')

    # Add graceful shutdown.
    signal.signal(signal.SIGTERM, partial(sig_handler, server))
    signal.signal(signal.SIGINT, partial(sig_handler, server))

    test_db()

    # TODO: Enable only in development mode.
    tornado.autoreload.start()
    for dir, _, files in os.walk('service'):
        [tornado.autoreload.watch(f'dir/{f}')
                for f in files if not f.startswith('.')]

    tornado.ioloop.IOLoop.current().start()
    logging.info('exiting...')
