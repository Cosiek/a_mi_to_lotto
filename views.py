#!/usr/bin/env python3
# encoding: utf-8

import re

import tornado.web

import js


class MainViewHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self.db = db

    def get(self):
        self.render("main.html", title="Hello, world")


class BaseUserViewHandler(tornado.web.RequestHandler):

    def initialize(self, db):
        self.db = db

        self.errors = {}
        self.ctx = {
            "title": "",
            "username": "",
            "code": "",
            "errors": self.errors,
        }

    def get(self):
        self.render("new_user.html", **self.ctx)

    def post(self):
        if self.validate():
            self.save()
            to = self.reverse_url("user", self.ctx['username'])
            self.redirect(to)
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
        elif username.lower() == "add":
            msg = "Nazwa \"add\" jest zastrzeżona"
        elif re.search(r'[\.\\\/,]', username):
            msg = 'Znaki "\\" "." "/" "," są zakazane.'
        elif self.db.get_player(username) is not None:
            msg = 'Gracz o podanym imieniu już istnieje.'

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
        filename = js.save_file(
                self.ctx["code"], self.ctx["username"])
        self.db.save_player(self.ctx["username"], filename)
        print("saving", self.ctx)


class NewUserViewHandler(BaseUserViewHandler):

    def initialize(self, db):
        super().initialize(db)
        self.ctx["title"] = "Nowy gracz"


class UserViewHandler(BaseUserViewHandler):

    def initialize(self, db):
        super().initialize(db)
        self.ctx["title"] = "Gracz"

    def get(self, username):
        user = self.db.get_player(username)
        if user is None:
            self.set_status(404)
            return
        self.ctx["username"] = user["name"]
        self.ctx["code"] = js.get_user_code(user["file"])
        super().get()

    def post(self, username):
        super().post()
