__metaclass__ = type

DOCUMENTATION = r'''
    inventory: steve
    version_added: "2.5"
    short_description: Filname is alan, but NAME on class is steve
    description:
        - Ignores whatever you give it
        - Returns inventory containing "alan"
'''

EXAMPLES = r'''
    # ansible -i 'host1.example.com, host2' -m user -a 'name=me state=absent' all
'''

from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = 'steve'

    def verify_file(self, host_list):
        return True  # looks good

    def parse(self, inventory, loader, host_list, cache=True):
        ''' doesnt parse the inventory file, but claims it did anyway '''
        super(InventoryModule, self).parse(inventory, loader, host_list)
        self.inventory.add_host('alan', group='ungrouped', port=8928)
