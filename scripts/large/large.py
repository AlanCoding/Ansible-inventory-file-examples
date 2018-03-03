#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import random
from collections import OrderedDict
import time
from copy import copy


def get_random_unicode(length):
    # https://stackoverflow.com/questions/1477294/generate-random-utf-8-string-in-python

    try:
        get_char = unichr
    except NameError:
        get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        ( 0x0021, 0x0021 ),
        ( 0x0023, 0x0026 ),
        ( 0x0028, 0x007E ),
        ( 0x00A1, 0x00AC ),
        ( 0x00AE, 0x00FF ),
        ( 0x0100, 0x017F ),
        ( 0x0180, 0x024F ),
        ( 0x2C60, 0x2C7F ),
        ( 0x16A0, 0x16F0 ),
        ( 0x0370, 0x0377 ),
        ( 0x037A, 0x037E ),
        ( 0x0384, 0x038A ),
        ( 0x038C, 0x038C ),
    ]

    alphabet = [
        get_char(code_point) for current_range in include_ranges
            for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(alphabet) for i in range(length))


"""
Maximum number of edges for groups

N = (N-1)*N/2

see the dag_max.py file
"""

r = {
    '_meta': {
        'hostvars': {}
    }
}

spec = os.getenv('INVENTORY_DIMENSIONS')

if spec is None:
    raise Exception('Set env var INVENTORY_DIMENSIONS to use this!')


split_spec = spec.split(':')

DEFAULTS = OrderedDict([
    ('hosts', 10),
    ('groups', 10),
    ('host_group', 0.1),
    ('group_group', 0.1),
    ('vars', 2),
    ('vars_len', 10)
])

params = {}

for i, key in enumerate(DEFAULTS.keys()):
    try:
        val = split_spec[i]
    except IndexError:
        val = DEFAULTS[key]
    if not isinstance(val, int) and val.endswith('k'):
        val = 1000*int(val.split('k')[0])
    try:
        val = int(val)
    except ValueError:
        val = float(val)
    params[key] = val


N = params['groups']
Ngc = (N-1)*N/2
Nhc = params['groups']*params['hosts']

fgg = 1.0*params['groups']/params['group_group']

fhg = 1.0*params['groups']/params['host_group']


DEBUG = False

if DEBUG:
    print ' params '
    print json.dumps(params, indent=4)
    print ' max group-group connections: ' + str(Ngc)
    print '   one-in-f   ' + str(fgg)
    print '      actual: ' + str(2*Ngc/fgg)
    print ' max host-group connections:  ' + str(Nhc)
    print '   one-in-f   ' + str(fhg)
    print '      actual: ' + str(Nhc/fhg)


# is_group_group_member = modulo_gen(fgg)
# is_host_group_member = modulo_gen(fhg)
if fgg < 1.0:
    print fgg
    raise Exception('Frequency of group-group membership is too large to make sense')
if fhg < 1.0:
    print fhg
    raise Exception('Frequency of host-group membership is too large to make sense')


def make_me_vars():
    '''
    Makes a blob of vars according to the parameters
    no special treatment, all vars are basically the same
    '''
    adict = {}
    for k in range(params['vars']):
        # Good heavens, what about collisions?!
        key = get_random_unicode(5)
        val = get_random_unicode(params['vars_len'])
        adict[key] = val
    return adict


# for performance reasons, use same vars for all resources
example_vars = make_me_vars()


# Groups building
start = time.time()
ig_mod = 0.0
Ngg = 0

for i in range(params['groups']):
    gdict = {'hosts': []}
    children = []
    start_ig_val = copy(ig_mod)
    while int(ig_mod - start_ig_val) < i:
        j = int(ig_mod % i)
        # A group will be a child of one in every <fgg> group
        # this only applies to the possible mappable groups, which are i<j
        # which actually makes it kind of complicated
        children.append('g{}'.format(j))
        ig_mod += fgg
    ig_mod -= i
    Ngg += len(children)
    gdict['children'] = children
    if params['vars']:
        gdict['vars'] = example_vars
    r['g{}'.format(i)] = gdict


r['all'] = {}
r['all']['vars'] = example_vars
r['all']['vars']['connection'] = 'local'


r['ungrouped'] = {
    'hosts': []
}

if DEBUG:
    print ''
    print ' group processing time ' + str(time.time() - start)
    print ' actual group-group: ' + str(Ngg)

# Hosts building
start = time.time()
Nhg = 0
ih_mod = 0.0

for i in range(params['hosts']):
    has_a_home = False
    hname = 'h{}'.format(i)
    if params['vars']:
        r['_meta']['hostvars'][hname] = example_vars
    start_ih_val = copy(ih_mod)
    while int(ih_mod - start_ih_val) < params['groups']:
        j = int(ih_mod % params['groups'])
        # A host will be a member of one in every <fhg> group
        ih_mod += fhg
        if not has_a_home:
            has_a_home = True
        Nhg += 1
        r['g{}'.format(j)]['hosts'].append(hname)
    if not has_a_home:
        r['ungrouped']['hosts'].append(hname)

if DEBUG:
    print ''
    print ' host processing time ' + str(time.time() - start)
    print ' actual host-group:  ' + str(Nhg)
    print ''


if not DEBUG:
    print json.dumps(r)


