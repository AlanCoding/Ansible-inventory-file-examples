#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

'''
This tests the acceptance of backslashes
\\f should be okay
\f is not necessarily okay, because json.dumps will not dump this
see:
https://github.com/ansible/awx/issues/524
so far, no problems with ansible-inventory have been found with this.
'''

print json.dumps({
    "foogroup": {
        "hosts": [
            "foobar"
        ]
    },
    "_meta": {
        "hostvars": {
            "foobar": {
                "host_specific_var": "ba\frrr",
                "from_issue": "H%]~7\f0$ and this... O'Jw\u00188\u0006\b... "
            }
        }
    }
}, indent=4)