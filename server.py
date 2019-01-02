#!/usr/bin/env python3
# encoding: utf-8

from os.path import dirname, join, realpath
import socket

import tornado.ioloop
import tornado.web
from tornado.web import url

import views
import db


CURRENT_DIR = dirname(realpath(__file__))


def run_periodic():
    print("Jup!")


def make_app():
    # init DB
    database = db.DBHandler()
    init = {
        "db": database
    }
    # instatate application
    return tornado.web.Application([
        url(r"/", views.MainViewHandler, init),
        url(r"/add", views.NewUserViewHandler, init),
        url(r"/(\w+)", views.UserViewHandler, init, name="user"),
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
