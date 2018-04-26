#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "group_host_name": {
                "foobar": "host_value"
            }
        }
    },
    "ungrouped": {
        "hosts": ["group_host_name"]
    },
    "group_host_name": {
        "hosts": [],
        "vars": {
            "foobar": "hello_world"
        }
    }
})