#!/usr/bin/env python
#
# URL=https://raw.githubusercontent.com/rmyers/ci_scripts/master/fail.py
# curl -s $URL | python

import subprocess
import os

WORKSPACE = os.environ['WORKSPACE']
CLEAN = 'cd {} && sudo chown -R jenkins:jenkins .'.format(WORKSPACE)

if __name__ == "__main__":
    subprocess.call(CLEAN, shell=True)
    subprocess.call('sudo reboot')
