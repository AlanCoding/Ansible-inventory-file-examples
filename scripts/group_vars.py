#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {"foovar": "baz"}
        }
    },
    "southeast": {
        "hosts": ["foobar"],
        "vars": {
            "group_var": "group_val",
            "group_var2": "group_val2"
        }
    }
})