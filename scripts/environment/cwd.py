#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os


cwd = os.getcwd()


print json.dumps({
    "_meta": {
        "hostvars": {}
    },
    "ungrouped": {
        "hosts": [cwd]
    },
})