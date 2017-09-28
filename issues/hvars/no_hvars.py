#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


print json.dumps({
    "_meta": {},
    "ungrouped": {
        "hosts": ["foobar"]
    }
})