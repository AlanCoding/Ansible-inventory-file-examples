# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    inventory: alan
    version_added: "2.5"
    short_description: Returns string "alan" for values of stuff
    description:
        - Ignores whatever you give it
        - Returns inventory containing "alan"
'''

EXAMPLES = r'''
    # ansible -i 'host1.example.com, host2' -m user -a 'name=me state=absent' all
'''

import os

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native
from ansible.parsing.utils.addresses import parse_address
from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = 'alan'

    def verify_file(self, host_list):
        return True  # looks good

    def parse(self, inventory, loader, host_list, cache=True):
        ''' doesnt parse the inventory file, but claims it did anyway '''
        super(InventoryModule, self).parse(inventory, loader, host_list)
        self.inventory.add_host('alan', group='ungrouped', port=8928)
