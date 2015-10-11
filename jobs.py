#!/usr/bin/env python
#
#  (re)Build the Jenkins jobs in dev2
#

import os
import sys
import argparse
import getpass
import xml.etree.ElementTree as ET
import jinja2
from jenkins import Jenkins
from run import TESTS
from run import PullRunner
from run import DIRECTORIES

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
JENKINS_CONFIGS = os.path.join(CURRENT_DIR, 'jobs')
TEMPLATE_DIR = os.path.join(CURRENT_DIR, 'templates')
ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
URL = 'http://cimaster-n01.prod.ord1.clouddb.rackspace.net:8080/'
RUN = 'https://raw.githubusercontent.com/rmyers/ci_scripts/master/run.py'
FAIL = 'https://raw.githubusercontent.com/rmyers/ci_scripts/master/fail.py'


def connection(username, password):
    return Jenkins(URL, username=username, password=password)


def config_filename(job_name):
    return os.path.join(JENKINS_CONFIGS, '{0}.xml'.format(job_name))


def get_jobs(conn, view):
    raw_config = conn.get_view_config(view)
    config = ET.fromstring(raw_config)
    jobs = [j.text for j in config.find('jobNames').getchildren()]
    return filter(None, jobs)


def store(args):
    conn = connection(args.username, args.password)
    for job_name in get_jobs(conn, args.view):
        job_config = conn.get_job_config(job_name)
        with open(config_filename(job_name), 'w') as config:
            config.write(job_config)


def reconfig(args):
    if not args.token:
        print('Please set the correct GITHUB_TOKEN in your env.')
        sys.exit(1)
    conn = connection(args.username, args.password)
    repos = DIRECTORIES.keys()
    repos.sort()
    context = {
        'run': RUN,
        'fail': FAIL,
        'project_list': ','.join([j.name for j in TESTS]),
        'repos': repos,
        'token': args.token,
    }
    tests = TESTS + [PullRunner(TESTS)]
    for test in tests:
        template = ENV.get_template(test.template)
        config = template.render(**context)
        try:
            conn.reconfig_job(test.name, config)
        except:
            conn.create_job(test.name, config)


class JenkinsConnection(object):

    def __init__(self, username, password):
        self.jenkins = Jenkins(URL, username=username, password=password)

    def store_job(self, job_name):
        job_config = self.jenkins.get_job_config(job_name)
        with open(self._config_filename(job_name), 'w') as config:
            config.write(job_config)

    def get_jobs(self, view):
        raw_config = self.jenkins.get_view_config(view)
        config = ET.fromstring(raw_config)
        jobs = [j.text for j in config.find('jobNames').getchildren()]
        return filter(None, jobs)


def main():
    parser = argparse.ArgumentParser(description='Make the jenkins jobs')
    # Default args
    parser.add_argument('--username', default=os.environ.get('JENKINS_USER'),
                        help='username defaults to $JENKINS_USER')
    parser.add_argument('--password', default=os.environ.get('JENKINS_PASS'),
                        help='password defaults to $JENKINS_PASS')
    parser.add_argument('--view', default='Dev2',
                        help='Jenking view to use (Dev2)')

    # Subcommands
    subparsers = parser.add_subparsers(
        title='commands',
        description='valid subcommands to run on jobs',
        help='"subcommand --help" for help')
    parser_store = subparsers.add_parser('store')
    parser_store.set_defaults(func=store)
    parser_reconfig = subparsers.add_parser('reconfig')
    parser_reconfig.add_argument(
        '--token', default=os.environ.get('GITHUB_TOKEN'),
        help='github api token defaults to $GITHUB_TOKEN')
    parser_reconfig.set_defaults(func=reconfig)

    args = parser.parse_args()
    if not args.username:
        args.username = raw_input('Jenkins Username:')
    if not args.password:
        args.password = getpass.getpass()

    args.func(args)

if __name__ == '__main__':
    main()
