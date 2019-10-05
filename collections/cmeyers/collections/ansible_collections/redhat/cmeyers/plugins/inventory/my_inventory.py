# Copyright (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    inventory: my_inventory
    short_description: Add a single host
    description: This plugin adds a single host specified by the hostname option
    extends_documentation_fragment:
        - inventory_cache
    options:
      plugin:
        description: plugin name (must be my_inventory)
        required: true
      hostname:
        description: Toggle display of stderr even when script was successful
        type: list
'''

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable
from ansible.utils.display import Display

display = Display()


class InventoryModule(BaseInventoryPlugin, Cacheable):

    NAME = 'my_inventory'

    def __init__(self, *args, **kwargs):
        super(InventoryModule, self).__init__()

        self._hosts = set()

    def parse(self, inventory, loader, path, cache=None):
        super(InventoryModule, self).parse(inventory, loader, path)

        config_data = loader.load_from_file(path, cache=cache)
        cache_key = self.get_cache_key(path)
        populate_cache = False
        results = {}
        if cache:
            cache = self.get_option('cache')
            if cache:
                try:
                    results = self._cache[cache_key]
                except KeyError:
                    populate_cache = True

        if not config_data.get('hostname'):
            raise AnsibleParserError("hostname was not specified")

        if not results:
            results['host'] = config_data.get('hostname')
            results['variables'] = {'foo': 'bar'}

        self.inventory.add_host(results['host'], 'all')
        for k, v in results['variables'].items():
            self.inventory.set_variable(results['host'], k, v)

        if cache and populate_cache:
            self._cache[cache_key] = results
