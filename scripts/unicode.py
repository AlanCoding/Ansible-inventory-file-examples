#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "not_unicode": {"host_var": "unicode here 🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉"},
            "🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉": {"host_vars": "some unicode here 🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉"}
        }
    },
    "all": {
        "vars": {
            "inventory_var": "this is an inventory var 🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉"
        }
    },
    "group 🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉": {
        "hosts": ["not_unicode", "🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉"],
        "vars": {
            "group_var": "this is group_var 🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉🐉"
        }
    }
})