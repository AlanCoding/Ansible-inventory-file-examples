#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


filename = os.environ['ENV_VAR']


with open(filename, 'r') as f:
    contents = f.read().strip()


print json.dumps({
    "_meta": {
        "hostvars": {}
    },
    "ungrouped": {
        "hosts": [contents]
    },
})