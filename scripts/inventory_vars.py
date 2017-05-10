#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# Credit for content goes to Jeff Geerling
# https://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible

print json.dumps({
    "group": {
        "hosts": [
            "192.168.28.71",
            "192.168.28.72"
        ],
        "vars": {
            "ansible_ssh_user": "johndoe",
            "ansible_ssh_private_key_file": "~/.ssh/mykey",
            "example_variable": "value"
        }
    },
    "_meta": {
        "hostvars": {
            "192.168.28.71": {
                "host_specific_var": "bar"
            },
            "192.168.28.72": {
                "host_specific_var": "foo"
            }
        }
    }
})