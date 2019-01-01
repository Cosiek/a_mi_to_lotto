#!/usr/bin/env python3
# encoding: utf-8

import subprocess


def is_valid(code):
    proc = subprocess.run(
                          ['js', '-e', code], 
                          stdout=subprocess.PIPE, 
                          universal_newlines=True)
    return (proc.returncode == 0 and
            not proc.stdout.strip())
