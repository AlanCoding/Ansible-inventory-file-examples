#!/usr/bin/env python
import json

'''
This shows an example of setting variables on the inventory as a whole
'''

print json.dumps({
    "foogroup": {
        "hosts": [
            "foobar",
            "barfoo"
        ]
    },
    "all": {
        "vars": {
            "all_inventory_var1": "value1",
            "all_inventory_var2": "value2"
        }
    },
    "_meta": {
        "hostvars": {
            "foobar": {
                "host_specific_var": "bar"
            },
            "barfoo": {
                "host_specific_var": "foo"
            }
        }
    }
}, indent=4)