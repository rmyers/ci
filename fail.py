#!/usr/bin/env python
#
# URL=https://raw.githubusercontent.com/rmyers/ci_scripts/master/fail.py
# curl -s $URL | python

import subprocess

FAB_CMD = '/usr/share/python/trove/bin/fab vm.clear'
FAB_CLEAN = '{fab} --fabfile=/Cloud-Database/fabfile.py'.format(fab=FAB_CMD)

if __name__ == "__main__":
    subprocess.call(FAB_CLEAN, shell=True)
