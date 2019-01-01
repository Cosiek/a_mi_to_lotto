#!/usr/bin/env python3
# encoding: utf-8

import tornado.web


class MainViewHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("main.html", title="Hello, world")


class UserViewHandler(tornado.web.RequestHandler):

    def get(self, username):
        self.render("main.html", title="Hello, " + username)
