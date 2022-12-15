# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: only_cache
    extends_documentation_fragment:
      - inventory_cache
    short_description: Caches the current inventory.
    description:
        - Does not load anything, reads current inventory state and puts it in cache.
    options:
        plugin:
            description: token that ensures this is a source file for the 'only_cache' plugin.
            required: True
            choices: ['alancoding.basic.only_cache', 'only_cache']
'''

EXAMPLES = r'''
    # inventory.config file in YAML format
    plugin: only_cache
'''

from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable
from ansible.inventory.manager import InventoryManager
from ansible.cli.inventory import InventoryCLI


class InventoryModule(BaseInventoryPlugin, Cacheable):
    """ caches the inventory loaded from the other sources """

    NAME = 'only_cache'

    def parse(self, inventory, loader, path, cache=False):
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)  # important gotcha

        # manager construction stolen from inventory_hostnames lookup plugin
        manager = InventoryManager(loader, parse=False)
        manager._inventory = inventory
        manager._sources = inventory.processed_sources

        inventory_cli = InventoryCLI(['ansible-inventory', '--list', '--export'])
        inventory_cli.inventory = manager
        inventory_cli.loader = loader

        top = inventory_cli._get_group('all')
        cache_key = self.get_cache_key(path)

        # some people will not like me for the following line, but you know
        # ▄▄█████████████████████████████─
        # ▀▀▀───▀█▄▀▄▀████▀──▀█▄▀▄▀████▀──
        # ────────▀█▄█▄█▀──────▀█▄█▄█▀────
        inventory.reconcile_inventory()

        self.cache[cache_key] = inventory_cli.json_inventory(top)
