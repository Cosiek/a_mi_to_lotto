#!/usr/bin/env python3
# encoding: utf-8

from os.path import dirname, join, realpath
import string
import subprocess

CURRENT_DIR = dirname(realpath(__file__))
SUBMITTED_DIR = join(CURRENT_DIR, "submitted")

JS_TEMPLATE_PTH = 'templates/js_template.js'


def is_valid(code):
    proc = subprocess.run(
                          ['js', '-e', code], 
                          stdout=subprocess.PIPE, 
                          universal_newlines=True)
    return (proc.returncode == 0 and
            not proc.stdout.strip())


def save_file(code, filename):
    filepath = join(SUBMITTED_DIR, filename + ".js")
    with open(filepath, 'w') as f:
        f.write(code)
    return filepath


def get_user_code(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    return code


def get_template():
    t = getattr(get_template, 't', None)
    if t is None:
        with open(JS_TEMPLATE_PTH, 'r') as f:
            t = string.Template(f.read())
            setattr(get_template, 't', t)
    return t


def save_execution_js_file(player, mapping):
    # read player submitted function
    with open(player['file'], 'r') as f:
        player_func = f.read()

    # prepare data for function
    mapping['funds'] = player['funds']
    template = get_template()
    output = player_func + template.substitute(mapping)

    # save file for execution
    filename = 'ready/' + player['name']
    with open(filename, 'w') as f:
        f.write(output)

    return filename


def execute(filename):
    return subprocess.run(['js', filename],
                          stdout=subprocess.PIPE,
                          universal_newlines=True)
