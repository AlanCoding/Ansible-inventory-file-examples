#!/usr/bin/env python
import json


data = {
    "_meta": {
        "hostvars": {
            "node01": {
                "ansible_host": "foo.invalid"
            }, 
            "node02": {
                "ansible_host": "bar.invalid"
            }, 
            "node03": {
                "ansible_host": "foobar.invalid"
            }
        }
    }, 
    "all": {
        "children": [
            "docker", 
            "gateway", 
            "ungrouped"
        ]
    }, 
    "docker": {
        "hosts": [
            "node01", 
            "node02", 
            "node03"
        ]
    }, 
    "gateway": {
        "hosts": [
            "node01"
        ]
    }, 
    "ungrouped": {}
}

print json.dumps(data)
