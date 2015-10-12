#!/bin/bash
#
#
#
# 1) Build a vm 'fab inova.boot:slave-03'
# 2) Log into it
# 3) Run this:
#    curl -s https://raw.githubusercontent.com/rmyers/ci_scripts/master/build_slave.sh | bash
# 4) Add the slave to jenkins (copy from DEV2-SLAVE01)

#
sudo adduser jenkins --home=/var/lib/jenkins

sudo su - jenkins

# TODO: Move these things to puppet
slave01=10.69.247.94
scp -r jenkins@$slave01:~/.ssh .
scp -r jenkins@$slave01:~/.bashrc .
