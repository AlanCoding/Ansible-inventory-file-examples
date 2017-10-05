### Ansible inventory plugins new in 2.4

Starting in 2.4, users are nudged to move to plugins as opposed to inventory
scripts.

http://docs.ansible.com/ansible/2.4/porting_guide_2.4.html#inventory-plugins

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/inventory/virtualbox.py#L39-L48

https://github.com/ansible/ansible/blob/devel/docs/docsite/rst/plugins/inventory.rst

#### Why aren't any hosts showing up?

Some plugin examples do not actually return content containing hosts, but
will modify content from another source. An example:

```
ansible-inventory -i plugins/example_hosts/constructed_hosts -i plugins/constructed.config --list
```

This shows `constructed.yml` sorting the hosts from `constructed_hosts` into
groups. Or, at least that's the idea.

### Examples of configuring plugins

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

### Using Openstack

You will have to mentally imagine that `/plugins/example_openstack/openstack.yml`
contains your real, valid, OpenStack credentials.
VERY IMPORTANT NOTE: you can not name this file something else. It must be
`openstack.yml` or `openstack.yaml` or it will fail without any clear reason
why.

The file `openstack.conf` is the configuration recommended in the 

Commands that do not work:

```
export ANSIBLE_INVENTORY_ENABLED=openstack
ansible-inventory -i plugins/example_openstack/openstack.yml --list
```

> [WARNING]: shade is required for the OpenStack inventory plugin.
> OpenStack inventory sources will be skipped.

fix this with:

```
pip install shade
```

In order to get it to work, you will also have to edit the file
`plugins/example_openstack/openstack.yml`, hard-coding in the path
of your clone of this repo. You also need to put in your own authentication
credentials into `plugins/example_openstack/clouds.yml`. With that all
in place:

```
export ANSIBLE_INVENTORY_ENABLED=openstack
ansible-inventory -i plugins/example_openstack/openstack.yml --list
```

This should produce the actual content.

