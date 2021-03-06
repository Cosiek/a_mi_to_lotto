#!/usr/bin/env python3
# encoding: utf-8

import json


class DBHandler():

    def __init__(self):
        self.data = None
        # try to read data from db.file
        self.db_filename = 'db.json'
        try:
            with open(self.db_filename, 'r') as f:
                self.data = json.load(f)
        # fallback to default values
        except:
            print("Unable to open DB file")  # TODO: use log
            self.data = self.get_default_data()

    def get_default_data(self):
        return {
            "players": {},
            "history": [],
        }

    def save_player(self, username, filepath):
        player = self.data['players'].get(
                username, self.get_new_player_dict())
        player["name"] = username
        player["file"] = filepath
        self.data['players'][username] = player

        self._save()

    def get_new_player_dict(self):
        import random
        return {
            "name": "",
            "file": "",
            "funds": 0,
            "balance": 0,  # random.randint(-1000, 1100),
        }

    def get_players(self, sort_key=None):
        p = self.data["players"].values()
        return p if sort_key is None else sorted(p, key=sort_key)

    def get_history(self):
        return self.data["history"]

    def get_player(self, player_name):
        return self.data["players"].get(player_name)

    def _save(self):
        with open(self.db_filename, 'w') as f:
            json.dump(self.data, f)

    def get_history(self):
        return self.data['history']

    def update(self, players, history):
        self.data['history'].append(history)

        for player in players:
            op = self.data['players'][player['name']]
            op['funds'] = player['funds']
            op['balance'] = player['balance']

        self._save()
