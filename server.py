#!/usr/bin/env python3
# encoding: utf-8

from os.path import dirname, join, realpath
import socket

import tornado.ioloop
import tornado.web
from tornado.web import url

import db
import lotto
import views


CURRENT_DIR = dirname(realpath(__file__))


def make_app(database):
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
    # init DB
    database = db.DBHandler()

    # prepare application
    port = 8888
    app = make_app(database)
    app.listen(port)
    
    # get server IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0] + ":" + str(port))
    s.close()
    
    # schedule tasks
    task = lambda: lotto.run(database)
    pc = tornado.ioloop.PeriodicCallback(task, 5000)
    pc.start()

    # start server
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
