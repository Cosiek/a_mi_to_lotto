#!/usr/bin/env python3
# encoding: utf-8

import tornado.web

import js


class MainViewHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("main.html", title="Hello, world")


class NewUserViewHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.errors = {}
        self.ctx = {
            "title": "Nowy użytkownik",
            "username": "",
            "code": "",
            "errors": self.errors,
        }

    def get(self):
        self.render("new_user.html", **self.ctx)

    def post(self):
        if self.validate():
            self.save()
            self.redirect("/" + self.ctx['username'])
        else:
            self.set_status(400)
            self.render("new_user.html", **self.ctx)

    def validate(self):
        is_valid = True
        for fieldname in ["username", "code"]:
            value = self.get_argument(fieldname)
            self.ctx[fieldname] = value
            validator_name = "validate_" + fieldname
            validator = getattr(self, validator_name)
            is_valid = validator(value) and is_valid
        return is_valid

    def validate_username(self, username):
        msg = ""
        if not username:
            msg = "Nazwa gracza jest wymagana."
        if username.lower() == "add":
            msg = "Nazwa \"add\" jest zastrzeżona"

        if msg:
            self.errors["username"] = msg
        return not bool(msg)

    def validate_code(self, code):
        msg = None
        if not code:
            msg = "To pole jest wymagane"
        elif not js.is_valid(code):
            msg = "Błąd walidacji js."

        if msg:
            self.errors["code"] = msg
        return not bool(msg)

    def save(self):
        print("saving", self.ctx)


class UserViewHandler(tornado.web.RequestHandler):

    def get(self, username):
        self.render("main.html", title="Hello, " + username)