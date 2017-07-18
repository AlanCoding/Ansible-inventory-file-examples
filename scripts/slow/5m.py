#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time


time.sleep(5*60)

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