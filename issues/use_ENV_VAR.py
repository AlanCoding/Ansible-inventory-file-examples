#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os


print json.dumps({
    "_meta": {
        "hostvars": {}
    },
    "all": {
        "hosts": [os.environ['ENV_VAR']]
    },
})