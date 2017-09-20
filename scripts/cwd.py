#!/usr/bin/env python
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