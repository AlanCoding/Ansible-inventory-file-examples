#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# This tests to see the effect of old scripts that delivered the port
# in different ways


print json.dumps({
    "_meta": {
        "hostvars": {
            "host_w_ssh_port": {"ansible_ssh_port": 8372},
            "host_w_ansible_port": {"ansible_port": 8252}
        }
    },
    "all": {
        "hosts": ["host_w_ssh_port", "host_w_ansible_port"]
    }
})