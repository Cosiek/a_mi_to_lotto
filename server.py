#!/usr/bin/env python3
# encoding: utf-8

import socket

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

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
    
    # start server
    loop.start()
