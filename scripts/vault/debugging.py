import yaml
import six


script_out = """all:
  children:
    ungrouped:
      hosts:
        foobar:
          should_be_artemis_here: !vault |
            $ANSIBLE_VAULT;1.2;AES256;alan
            30386264646430643536336230313232653130643332356531633437363837323430663031356364
            3836313935643038306263613631396136663634613066650a303838613532313236663966343433
            37636234366130393131616631663831383237653761373533363666303361333662373664336261
            6136313463383061330a633835643434616562633238383530356632336664316366376139306135
            3534"""

# --- the YAML docs ---

# class Monster(yaml.YAMLObject):
#     yaml_tag = u'!vault'
#     def __init__(self, node):
#         print ' args kwargs ' + str(node)# + str(kwargs)
#         self.node = node
# 
#     def __repr__(self):
#         return str(self.node)

# second example

class Dice(tuple):
    def __new__(cls, a, b):
        return tuple.__new__(cls, [a, b])
    def __repr__(self):
        return "Dice(%s,%s)" % self


def dice_representer(dumper, data):
    return dumper.represent_scalar(u'!dice', u'%sd%s' % data)


def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)


yaml.add_representer(Dice, dice_representer)
yaml.add_constructor(u'!dice', dice_constructor)


print yaml.dump({'gold': Dice(10,6)})
print yaml.load("""initial hit points: !dice 8d4""")



class NaiveVault:
    def __init__(self, data):
        self.data = data
    def __repr__(self):
        return six.text_type(self.data)


print NaiveVault('hello world')


def vault_representer(dumper, data):
    return dumper.represent_scalar(u'!vault', six.text_type(data))


def vault_constructor(loader, node):
    value = loader.construct_scalar(node)
    return NaiveVault(value)


yaml.add_representer(NaiveVault, vault_representer)
yaml.add_constructor(u'!vault', vault_constructor)


# --- the Ansible method ---

# from yaml.constructor import SafeConstructor
# 
# class AnsibleConstructor(SafeConstructor):
# 
#     def construct_vault_encrypted_unicode(self, node):
#         value = self.construct_scalar(node)
#         return str(value)
# 
# yaml.add_constructor(
#     u'!vault',
#     AnsibleConstructor.construct_vault_encrypted_unicode)



python_out = yaml.load(script_out)


print ' python output '
print python_out

print ' dumped output '
print yaml.dump(python_out, default_flow_style=False)

print ' original script out '
print script_out


print ' again, using safe_load '
yaml.SafeLoader.add_constructor(u'!vault', vault_constructor)

python_out = yaml.safe_load(script_out)

