#!/usr/bin/env python
#
# WARNING! This Script is automatically injected by the PR job builder.
# Any changes made directly in jenkins will be overwritten on the
# next run of the builder script.
#

import subprocess
import os

WORKSPACE = os.environ['WORKSPACE']
CLEAN = 'cd {} && sudo chown -R jenkins:jenkins .'.format(WORKSPACE)

if __name__ == "__main__":
    subprocess.call(CLEAN, shell=True)
