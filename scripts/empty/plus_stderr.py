#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import sys


# Write to standard error
print('TEST', file=sys.stderr)

print(json.dumps({
    "_meta": {
        "hostvars": {}
    }
}))