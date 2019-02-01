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

import mysql.connector
from mysql.connector import errorcode

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

def make_app():
    return tornado.web.Application([
            (r'/', MainHandler, dict(service=echo.make_service()))
        ])

def test_db():
    try:
        config = {
            'user': 'john',
            'password': '123456',
            'host': '127.0.0.1',
            'database': 'python_test'
        }
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ADDRESS_DENIED_ERROR:
            print('invalid database username or credentials')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('database does not exist')
        else:
            print(err)

    cursor = cnx.cursor()
    try:
        cursor.execute('select 1 + 1')
        for (data) in cursor:
            print('cursor data', data)
        cursor.close()
    except mysql.connector.Error as err:
        print(err)

    cnx.close()
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
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)
    print(f'listening to port*:{port}. press ctrl + c to cancel')
    signal.signal(signal.SIGTERM, partial(sig_handler, server))
    signal.signal(signal.SIGINT, partial(sig_handler, server))

    test_db()

    # TODO: Add graceful shutdown tornado.
    # TODO: Enable only in development mode.
    tornado.autoreload.start()
    for dir, _, files in os.walk('service'):
        [tornado.autoreload.watch(f'dir/{f}')
                for f in files if not f.startswith('.')]

    tornado.ioloop.IOLoop.current().start()
    logging.info('exiting...')
