#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {}
        }
    },
    "all": {
        "hosts": ["foobar"]
    }
})