#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml


print yaml.dump({
    "_meta": {
        "hostvars": {
            "foobar": {}
        }
    },
    "ungrouped": {
        "hosts": ["foobar"]
    }
})