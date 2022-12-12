# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: destructed
    version_added: "2.14"
    short_description: Uses a host_pattern to delete hosts that you do not want in inventory.
    description:
        - Give a host pattern.
        - All hosts not matching that host pattern will be deleted.
    options:
        plugin:
            description: token that ensures this is a source file for the 'constructed' plugin.
            required: True
            choices: ['alancoding.basic.destructed', 'destructed']
        host_pattern:
            description:
                - An Ansible host pattern like limit to ansible-playbook, all hosts not in pattern will be removed.
            required: true
            default: ''
            type: str
            version_added: '2.14'
'''

EXAMPLES = r'''
    # inventory.config file in YAML format
    plugin: destructed
    host_pattern: host1
'''

import os

from ansible import constants as C
from ansible.errors import AnsibleParserError, AnsibleOptionsError
from ansible.inventory.helpers import get_group_vars
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.module_utils._text import to_native
from ansible.utils.vars import combine_vars
from ansible.vars.fact_cache import FactCache
from ansible.vars.plugins import get_vars_from_inventory_sources

from ansible.inventory.manager import InventoryManager


class InventoryModule(BaseInventoryPlugin, Constructable):
    """ destroys hosts you do not want using a host_pattern """

    NAME = 'destructed'

    def __init__(self):

        super(InventoryModule, self).__init__()

        self._cache = FactCache()

    def parse(self, inventory, loader, path, cache=False):
        ''' parses the inventory file '''

        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self._read_config_data(path)

        host_pattern = self.get_option('host_pattern')
        if not host_pattern:
            return

        # manager construction stolen from inventory_hostnames lookup plugin
        manager = InventoryManager(loader, parse=False)
        manager._inventory = inventory


        keep_list = set(host.name for host in manager.get_hosts(pattern=host_pattern))

        for host in manager.get_hosts():
            if host.name not in keep_list:
                inventory.remove_host(host)
