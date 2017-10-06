#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'afile.txt')


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