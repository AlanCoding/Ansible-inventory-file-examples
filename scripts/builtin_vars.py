#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {
                "ansible_host": "baz",
                "ansible_port": 8013
            }
        }
    },
    "ungrouped": {
        "hosts": [
            "foobar"
        ]
    }
})