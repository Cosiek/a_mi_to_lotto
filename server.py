#!/usr/bin/env python3
# encoding: utf-8

from os.path import dirname, join, realpath
import socket

import tornado.ioloop
import tornado.web

import views


CURRENT_DIR = dirname(realpath(__file__))


def run_periodic():
    print("Jup!")


def make_app():
    return tornado.web.Application([
        (r"/", views.MainViewHandler),
        (r"/(\w+)", views.UserViewHandler),
        ],
        template_path=join(CURRENT_DIR, "templates"),
        debug=True
    )


if __name__ == "__main__":
    port = 8888
    app = make_app()
    app.listen(port)
    
    # get server IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0] + ":" + str(port))
    s.close()
    
    # get loop
    loop = tornado.ioloop.IOLoop.current()
    
    # schedule tasks
    pc = tornado.ioloop.PeriodicCallback(run_periodic, 5000)
    pc.start()

    # start server
    loop.start()
