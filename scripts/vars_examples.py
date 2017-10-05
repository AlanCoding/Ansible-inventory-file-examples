#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {
                "foovar": "baz",
                "ansible_port": 8013
            }
        }
    },
    "southeast": {
        "hosts": ["foobar"],
        "children": ["child_group"],
        "vars": {
            "southest_group_var": "southeast_group_var_value"
        }
    },
    "child_group": {
        "hosts": ["child_group_host"],
        "vars": {
            "child_group_var": "child_group_value"
        }
    },
    "all": {
        "hosts": ["all_group_host"],
        "vars": {
            "all_inventory_var": "all_inventory_var_value"
        }
    },
    "ungrouped": {
        "hosts": ["ungrouped_host"],
        "vars": {
            "ungrouped_group_var": "ungrouped_group_var_value"
        }
    }
}, indent=4)
