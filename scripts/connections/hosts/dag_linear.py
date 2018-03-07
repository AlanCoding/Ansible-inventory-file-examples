#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

"""
Maximum number of edges in group relationships

N = (N-1)*N/2
example of 5
N = 4*5/2 = 20/2 = 10

https://stackoverflow.com/questions/11699095/how-many-edges-can-there-be-in-a-dag
"""

r = {
    '_meta': {
        'hostvars': {}
    }
}

N = int(os.getenv('NUMBER_HOSTS'))
all_groups = bool(os.getenv('ALL_GROUPS', False))

Ng = N

all_hosts = ['h{}'.format(i) for i in range(N)]

for i in range(Ng):
    group_name = 'g{}'.format(i)
    if all_groups or i == Ng-1:
        host_list = all_hosts
    else:
        host_list = []
    if i == 0:
        r[group_name] = {
            'hosts': host_list,
            'children': []
        }
    else:
        r[group_name] = {
            'hosts': host_list,
            'children': ['g{}'.format(i-1)]
        }


for i in range(N):
    hostname = 'h{}'.format(i)
    r['_meta']['hostvars'][hostname] = {}


print json.dumps(r)