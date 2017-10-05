#!/usr/bin/env python
import json
inventory = {
    'group-1': ['host1', 'host2']
}
print json.dumps(inventory)