import json
import yaml
import six


YAML_DATA = '''
vars_secret_funky_json: !vault |
    $ANSIBLE_VAULT;1.2;AES256;alan_host
    35356666616633303337313766346562613961313262333530663432393965303736653334306433
    6239666265343936343462653836386162343234353961330a306665396665353364613863316362
    66646663313737393763383565333237316663666339623063646666646261643338616261633330
    3634313634666264620a383632386661653330326435633861333031643334643237366430313733
    3733
'''

JSON_DATA = '''
{
    "vars_secret_funky_json": {
        "__ansible_vault": "$ANSIBLE_VAULT;1.2;AES256;alan_host\\n35356666616633303337313766346562613961313262333530663432393965303736653334306433\\n6239666265343936343462653836386162343234353961330a306665396665353364613863316362\\n66646663313737393763383565333237316663666339623063646666646261643338616261633330\\n3634313634666264620a383632386661653330326435633861333031643334643237366430313733\\n3733\\n"
    }
}
'''


class VaultData:
    def __init__(self, value):
        self.value = value


class VaultDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = self.object_hook
        super(VaultDecoder, self).__init__(*args, **kwargs)

    def object_hook(self, pairs):
        for key in pairs:
            value = pairs[key]
            if key == '__ansible_vault':
                return VaultData(value)

        return pairs


class VaultEncoder(json.JSONEncoder):
    '''
    Simple encoder class to deal with JSON encoding of Ansible internal types
    '''
    def default(self, o):
        if isinstance(o, VaultData):
            return {'__ansible_vault': o.value}
        return json.JSONEncoder.default(self, o)


class SafeStringDumper(yaml.SafeDumper):

    def represent_vault_data(self, data):
        return self.represent_scalar('!vault', data.value, style='|')


class SafeLoader(yaml.Loader):

    def construct_yaml_vault(self, node):
        value = self.construct_scalar(node)
        return VaultData(value)


SafeLoader.add_constructor(
    u'!vault',
    SafeLoader.construct_yaml_vault
)


SafeStringDumper.add_representer(
    VaultData,
    SafeStringDumper.represent_vault_data
)


jdata = json.loads(JSON_DATA, cls=VaultDecoder)
print(yaml.dump(jdata, Dumper=SafeStringDumper, default_flow_style=False))

ydata = yaml.load(YAML_DATA, Loader=SafeLoader)
print(json.dumps(ydata, cls=VaultEncoder, indent=4))
