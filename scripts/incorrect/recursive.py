#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {
        "hostvars": {
            "foobar": {"foovar": "baz"},
            "foo.com": {"baz": "var"}
        }
    },
    "southeast": {
        "hosts": ["foobar"],
        "children": ["westeast"]
    },
    "westeast": {
        "hosts": ["foo.com"],
        "children": ["southeast"]
    }
})