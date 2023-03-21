#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


data = {
    "all": {
        "hosts": [
            "host2"
        ],
        "children": [
            "groupA",
            "groupB"
        ]
    },
    "groupA": {
        "children": [
            "groupB"
        ],
        "vars": {
            "filter_var": "filter_val"
        }
    },
    "groupB": {
        "hosts": [
            "host1"
        ]
    },
    "_meta": {
        "hostvars": {
            "host1": {
                "ansible_host": "localhost",
                "ansible_connection": "local",
                "ansible_python_interpreter": "{{ ansible_playbook_python }}"
            },
            "host2": {
                "ansible_host": "localhost",
                "ansible_connection": "local",
                "ansible_python_interpreter": "{{ ansible_playbook_python }}"
            }
        }
    }
}


print(json.dumps(data, indent=2))
