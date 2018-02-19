#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "ahost": {"host_var": 4}
        }
    },
    "all": {
        "vars": {
            "inventory_var": 1
        }
    },
    "agroup": {
        "hosts": ["ahost"],
        "vars": {
            "group_var": 2
        }
    }
})