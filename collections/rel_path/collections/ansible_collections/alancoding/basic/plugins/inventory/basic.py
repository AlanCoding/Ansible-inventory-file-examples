DOCUMENTATION = r'''
    inventory: basic
    name: Inventory Plugin Basics
    plugin_type: inventory
    author:
      - Alan Rominger (@AlanCoding)
      - Will Tome (@willtome)
    short_description: Creates a number of hosts based on the input “count”.
    version_added: "2.10"
    description:
        - Demonstrates basics of a custom inventory plugin.
    options:
        count:
            description: The number of hosts and groups to make.
            type: integer
            required: True
        password:
            description: Password to put in hostvars b64 encoded.
            type: string
            secret: true
            default: foo
            env:
                - name: BASIC_PASSWORD
    requirements:
        - python >= 3.4
'''

EXAMPLES = r'''
# create 4 sub-groups and hosts
plugin: basic
count: 4
'''

# Ansible internal request utilities
from ansible.module_utils.six.moves.urllib.parse import urljoin
from ansible.module_utils.urls import Request, ConnectionError, urllib_error

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin

from base64 import b64encode


import json


def _hash_password(password):
    return str(b64encode(bytes(password, encoding='utf8')), encoding='utf8')


class InventoryModule(BaseInventoryPlugin):

    NAME = 'basic'

    def parse(self, inventory, loader, path, cache=True):  # Plugin interface (2)
        super(InventoryModule, self).parse(inventory, loader, path)
        self._read_config_data(path)

        root_group_name = self.inventory.add_group('root-group')  # Inventory interface (3)

        for i in range(self.get_option('count')):
            group_name = self.inventory.add_group('group_%s' % i)  # Inventory interface (3)
            self.inventory.add_child(root_group_name, group_name)  # Inventory interface (5)
            host_name = self.inventory.add_host('host_%s' % i)  # Inventory interface (1)
            self.inventory.add_child(group_name, host_name)  # Inventory interface (4)

        self.inventory.set_variable(
            root_group_name, 'hashed_password', _hash_password(self.get_option('password'))
        )  # inventory interface (2)
