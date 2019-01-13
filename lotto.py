#!/usr/bin/env python3
# encoding: utf-8

import json
import string
import random
import subprocess

import js

# lotto logic

BET_COST = 7


def get_winning_numbers():
    return set(random.sample(range(1, 50), 6))


def worth(bet, numbers):
    hits = len(numbers.intersection(bet))
    if hits == 3:
        return 24
    elif hits == 4:
        return 170
    elif hits == 5:
        return 5300
    elif hits == 6:
        return 4000000
    else:
        return 0

# helpers

def bet_is_valid(bet):
    try:
        return (isinstance(bet, list) and
                len(bet) == 6 and
                all(0 < v < 50 for v in bet))
    except:
        return False


def validate_bets(bets):
    try:
        bets = json.loads(bets)
    except:
        return False

    v = all(bet_is_valid(bet) for bet in bets)
    return bets if v else False


# running

def run(db):
    # get winning numbers
    numbers = get_winning_numbers()

    # prepare some args for js function
    mapping = {
        'history': db.get_history(),
        'cost': BET_COST
    }

    his_hlp = []  # history helper

    # use a copy of players data
    players = []

    # iterate over players
    for player_ in db.get_players():
        # use this to prevent race conditions when saving
        player = player_.copy()
        players.append(player)

        # player earned some money
        player["funds"] += 100

        filename = js.save_execution_js_file(player, 
                                             mapping)

        # execute a file in js
        bets = js.execute(filename)

        bets = validate_bets(bets)

        if not bets:
            # not sure what else to do
            continue

        funds = player['funds']
        for bet in bets:
            # valdate number of bets
            if funds - BET_COST < 0:
                break

            money = worth(bet, numbers)
            player['funds'] += money - BET_COST
            player['balance'] += money - BET_COST
            if money > 0:
                his_hlp.append((player['name'], bet, money))

    # prepare history input
    his_hlp.sort(key=lambda x: -x[2])
    history = {
        "numbers": list(numbers),
        "winnings": his_hlp,
    }

    db.update(players, history)
