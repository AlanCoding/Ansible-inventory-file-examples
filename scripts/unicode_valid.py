#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print(json.dumps({
    "_meta": {
        "hostvars": {
            "not_unicode": {"host_var": "unicode here 日本語"}
        }
    },
    "all": {
        "vars": {
            "inventory_var": "this is an inventory var 日本語"
        }
    },
    "group_日本語": {
        "hosts": ["not_unicode"],
        "vars": {
            "group_var": "this is group_var 日本語"
        }
    }
}))