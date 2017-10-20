### Ansible inventory plugins new in 2.4

Starting in 2.4, users are nudged to move to plugins as opposed to inventory
scripts.

Some links on the subject:

 - http://docs.ansible.com/ansible/2.4/porting_guide_2.4.html#inventory-plugins
 - https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/inventory/
 - https://github.com/ansible/ansible/blob/devel/docs/docsite/rst/plugins/inventory.rst
   - https://docs.ansible.com/ansible/devel/plugins/inventory.html

The old inventory scripts:

 - https://github.com/ansible/ansible/blob/devel/contrib/inventory/

### Simple example of configuring plugins

Turn off a needed plugin, and watch the inventory fail.

```
export ANSIBLE_INVENTORY_ENABLED=script
ansible-inventory -i official/inventory.ini --list
```

> [WARNING]: Unable to parse <...>/official/inventory.ini as an inventory source

In this example, it can not parse the contents of the file, because the
ini inventory plugin is not available.

```
export ANSIBLE_INVENTORY_ENABLED=ini
ansible-inventory -i official/inventory.ini --list
```

That works.

Ansible will not accept an invalid plugin name.

```
export ANSIBLE_INVENTORY_ENABLED=foobar
```

> [WARNING]: Failed to load inventory plugin, skipping foobar

#### The "constructed" built-in plugin

Some plugin examples do not actually return content containing hosts, but
will modify content from another source. The "constructed" plugin is the
most important example of this at the current time:

```
export ANSIBLE_INVENTORY_ENABLED=ini,constructed
ansible-inventory -i plugins/example_hosts/constructed_hosts -i plugins/constructed.config --list
```

The plugins list allows the first file (defining the hosts) to be interpreted
via the `ini` plugin. Then the 2nd inventory given by the `-i` flag
will grok the contents of `constructed.config`, which modifies the inventory
contents dynamically.

`constructed.config` sorts the hosts from `constructed_hosts` into
groups. As a case-in-point, the host `websomething` is put into the
`webservers` because its name starts with "web". This is a rule defined
in the `constructed.config` file.

The "constructed" inventory must be used _after_ any other inventories that
it is intended to operate on in the CLI args.

### Using Openstack

In order to get this to work, you will have to edit the file
`plugins/example_openstack/openstack.yml`, hard-coding in the path
of your clone of this repo.

VERY IMPORTANT NOTE: you can not name this file something else. It must be
`openstack.yml` or `openstack.yaml` or it will fail without any clear reason
why.

You also need to put in your own authentication
credentials into `plugins/example_openstack/clouds.yml`.

Additional pre-requisites are that you install the `shade` library, and
that you specifically enable the openstack plugin. That is covered in the
following lines:

```
pip install shade
export ANSIBLE_INVENTORY_ENABLED=openstack
ansible-inventory -i plugins/example_openstack/openstack.yml --list
```

This should produce the actual content.

#### Verification

We can verify this content by comparing it to the output of ansible-playbook:

```
ansible-playbook -i plugins/example_openstack/openstack.yml debugging/hostvars_print.yml
```

Also, we can compare the output to the old inventory script.

```
unset ANSIBLE_INVENTORY_ENABLED
export OS_CLIENT_CONFIG_FILE=<cwd>/plugins/example_openstack/clouds.yml
ansible-inventory -i <ansible source location>/contrib/inventory/ec2.py --list
```

Current testing shows that these methods produce _very near_ the same data,
although not exactly the same.

### User-defined Plugin

In this case, you have written a plugin yourself, unlike the previous examples
which all used plugins vendored with Ansible.

```
export ANSIBLE_INVENTORY_PLUGINS=$(PWD)/plugins/user_plugins/
ansible-doc -t inventory -l
ansible-doc -t inventory alan
```

(note, the `ansible-doc` commands are fixed as of
[Ansible PR #31996](https://github.com/ansible/ansible/pull/31996),
Ansible 2.4.2 or higher is needed)

If that is working, it should be feasible to do the following:

```
export ANSIBLE_INVENTORY_ENABLED=alan
ansible-inventory -i top_level_file.ini --list
```

No matter what inventory file you give it in this case, the output should
just have a host named "alan".

#### Relative path

If you have a folder named `inventory_plugins` inside your current
working directory, Ansible will use that.

```
cd plugins/user_plugins_rel/
export ANSIBLE_INVENTORY_ENABLED=alan
ansible-inventory -i foobar.ini --list
```

result:

```
ansible-inventory -i foobar.ini --list
{
    "_meta": {
        "hostvars": {
            "alan": {
                "ansible_port": 8928
            }
        }
    }, 
    "all": {
        "children": [
            "ungrouped"
        ]
    }, 
    "ungrouped": {
        "hosts": [
            "alan"
        ]
    }
}
```
