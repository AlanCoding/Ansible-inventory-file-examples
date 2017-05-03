#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


print json.dumps({
    "_meta": {
        "hostvars": {}
    },
    "ungrouped": {
        "hosts": [os.environ['ENV_VAR']]
    },
})