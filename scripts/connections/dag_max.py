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

N = int(os.getenv('NUMBER_GROUPS'))

for i in range(N):
    group_name = 'g{}'.format(i)
    r[group_name] = {
        'hosts': [],
        'children': ['g{}'.format(j) for j in range(i)]
    }

print json.dumps(r)