### Ansible inventory plugins new in 2.4

Starting in 2.4, users are nudged to move to plugins as opposed to inventory
scripts.

http://docs.ansible.com/ansible/2.4/porting_guide_2.4.html#inventory-plugins

https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/inventory/virtualbox.py#L39-L48

#### Why aren't any hosts showing up?

Some plugin examples do not actually return content containing hosts, but
will modify content from another source. An example:

```
ansible-inventory -i plugins/example_hosts/constructed_hosts -i plugins/constructed.yml --list
```

This shows `constructed.yml` sorting the hosts from `constructed_hosts` into
groups. Or, at least that's the idea.
