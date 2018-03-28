#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import os
import base64
import sys

N = os.getenv('INVENTORY_STDERR')
if not N:
    N = 5000000
err = base64.b64encode(os.urandom(int(N)))

print('{"foooooo')

print(err, file=sys.stderr)
