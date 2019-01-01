#!/usr/bin/env python3
# encoding: utf-8

import tornado.web


class MainViewHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")
        
        
class UserViewHandler(tornado.web.RequestHandler):

    def get(self, username):
        self.write("Hello, " + username)
