#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import six

DEBUG = False


script_out = """_meta:
  hostvars:
    foobar:
        should_be_artemis_here: !vault |
          $ANSIBLE_VAULT;1.2;AES256;alan
          30386264646430643536336230313232653130643332356531633437363837323430663031356364
          3836313935643038306263613631396136663634613066650a303838613532313236663966343433
          37636234366130393131616631663831383237653761373533363666303361333662373664336261
          6136313463383061330a633835643434616562633238383530356632336664316366376139306135
          3534
ungrouped:
  hosts:
  - foobar"""

class NaiveVault:
    def __init__(self, data):
        if DEBUG:
            print ' initial data ' + str(data)
        self.data = data
    def __repr__(self):
        if DEBUG:
            print ' builtin representer ' + str(self.data)
        return six.text_type(self.data)



def vault_representer(dumper, data):
    if DEBUG:
        print ' representer data ' + str(data)
    r = dumper.represent_scalar(u'!vault', six.text_type(data), style='|')
    if DEBUG:
        print '  prepared to represent: ' + str(r)
    return r


def vault_constructor(loader, node):
    value = loader.construct_scalar(node)
    if DEBUG:
        print ' constructing value ' + str(value)
    return NaiveVault(value)


yaml.add_representer(NaiveVault, vault_representer)
yaml.add_constructor(u'!vault', vault_constructor)

python_out = yaml.load(script_out)
print yaml.dump(python_out, default_flow_style=False)

