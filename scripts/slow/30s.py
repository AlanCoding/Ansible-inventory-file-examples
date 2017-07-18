#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time


time.sleep(30)

print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {}
        }
    },
    "ungrouped": {
        "hosts": ["foobar"]
    }
})