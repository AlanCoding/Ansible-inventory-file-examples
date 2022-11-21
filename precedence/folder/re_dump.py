#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json


data_file = os.path.join(os.path.dirname(__file__), 'output.json')

with open(data_file, 'r') as f:
    content = f.read()

data = json.loads(content)

print(json.dumps(data, indent=2))
