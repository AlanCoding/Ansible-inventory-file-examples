#!/usr/bin/env python
import json

print json.dumps({
    "_meta": {
        "hostvars": {},
    },
    "foo": {
        "hosts": []
    }
})