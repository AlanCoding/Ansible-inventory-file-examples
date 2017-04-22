#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
inventory = dict()
inventory["group-1"] = list()
inventory["group-1"].append("host-1")
inventory["group-1"].append("host-2")
print json.dumps(inventory)