#!/usr/bin/env python3
import json
inventory = {
    'group-1': ['host1', 'host2']
}
print json.dumps(inventory)