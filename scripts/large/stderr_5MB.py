#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import os
import base64
import sys

err = base64.b64encode(os.urandom(5000000))


d = {
    "_meta": {
        "hostvars": {
            "foobar": {}
        }
    },
    "ungrouped": {
        "hosts": ["foobar"]
    }
}

print(json.dumps(d))

print(err, file=sys.stderr)
