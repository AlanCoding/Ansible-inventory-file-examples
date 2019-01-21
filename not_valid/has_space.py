#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# includes a host name that has a space in it
print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {}
        }
    },
    "ungrouped": {
        "hosts": ["foo bar"]
    }
})