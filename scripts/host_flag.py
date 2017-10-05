#!/usr/bin/env python

'''
This script returns variables specific to a host if given --host <hostname> option
'''

from argparse import ArgumentParser
import json


parser = ArgumentParser()
parser.add_argument(
    '--list', dest='list_instances', action='store_true', default=True,
    help='List instances (default: True)'
)

parser.add_argument(
    '--host', dest='requested_host',
    help='Get all the variables about a specific instance'
)

args = parser.parse_args()

if args.requested_host:
    print json.dumps({
        'foobar': {'foovar': 'foovalue'},
        'host1': {'host1var': 'val'}
    }.get(args.requested_host, {}))
elif args.list_instances:
    print json.dumps({
        'ungrouped': ['foobar', 'host1']
    })
else:
    raise Exception('I do not know what to do.')
