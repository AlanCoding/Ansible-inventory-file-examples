### Combination of file and encrypted vars

The scenario this example is concerned with can be ran by this:

```
ansible-inventory -i vault/file_vars/inventory.ini --list --export
```

Without other changes, this throws an error in Ansible 2.14.
The inventory has two groups in it, and two files in related `group_vars/` folder.
 - the `raleigh` file contains a whole file encrypted by ansible-vault
 - the `unencrypted` file contains an unrelated plain-text variable

Some discussion about this case can be found at the issue:
https://github.com/ansible/awx/issues/12829

It is possible to change the behavior with basic ansible-core to not throw
an error with this usage:

```
ANSIBLE_VARS_ENABLED='' ansible-inventory -i vault/file_vars/inventory.ini --list --export
```

However, this fails to pull in variables from the `unencrypted` group.

https://docs.ansible.com/ansible/latest/plugins/vars.html

> You can activate a custom vars plugin by either dropping it into a
> vars_plugins directory adjacent to your play, inside a role,
> or by putting it in one of the directory sources configured in ansible.cfg.

The second part of this about `ansible.cfg` probably refers
to the setting `DEFAULT_VARS_PLUGIN_PATH` documented in the related link.
Environment variable for this is `ANSIBLE_VARS_PLUGINS`.

A custom plugin is tested as a partial solution to the problem described
in the AWX issue here. This is named `host_group_vars_reduced` and is
housed in the `vault/file_vars/plugins` folder from the top-level of this repo.
Run this with:

```
ANSIBLE_HOST_GROUP_VARS_VAULT_ERROR_BEHAVIOR=warn ANSIBLE_VARS_PLUGINS=vault/file_vars/plugins ANSIBLE_VARS_ENABLED=host_group_vars_reduced ansible-inventory -i vault/file_vars/inventory.ini --list --export
```

This avoids decrypting the `raleigh` vars but does pull in the `unencrypted` vars,
which is what the objective is here.

```JSON{
    "_meta": {
        "hostvars": {}
    },
    "all": {
        "children": [
            "raleigh",
            "unencrypted",
            "ungrouped"
        ]
    },
    "raleigh": {
        "hosts": [
            "host1",
            "host2"
        ]
    },
    "unencrypted": {
        "hosts": [
            "host3"
        ],
        "vars": {
            "airport_code": "RDU"
        }
    }
}
```
