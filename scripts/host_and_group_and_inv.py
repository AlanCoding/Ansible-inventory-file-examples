#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {"host_var": "this is foobar"}
        }
    },
    "all": {
        "vars": {
            "inventory_var": "this is an inventory with host and group and inventory vars"
        }
    },
    "southeast": {
        "hosts": ["foobar"],
        "vars": {
            "group_var": "this is southeast, host and humid"
        }
    }
})