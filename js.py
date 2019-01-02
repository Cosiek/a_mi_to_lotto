#!/usr/bin/env python3
# encoding: utf-8

from os.path import dirname, join, realpath
import subprocess

CURRENT_DIR = dirname(realpath(__file__))
SUBMITTED_DIR = join(CURRENT_DIR, "submitted")


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
