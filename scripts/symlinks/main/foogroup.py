#!/usr/bin/env python
import json

print json.dumps({
    "_meta": {
        "hostvars": {
            'afoo': {}
        },
    },
    "foo": {
        "hosts": ['afoo']
    }
})