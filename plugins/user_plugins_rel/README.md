### User-defined plugin files

Some issues with this were originally described in:

https://github.com/ansible/ansible/issues/51033

Conceptually, this should work with the command:

```
ansible-inventory -i foobar.ini --list
```

when ran from inside of this folder.

#### Running from project root

As of right now, `--playbook-dir` does not yet affect the search paths
for Ansible config files. That means that you cannot make use of the
`ansible.cfg` in this folder unless you are running from this folder.

Thus, to run this example from project root, you will need to specify
the _plugin_ manually.

```
ANSIBLE_INVENTORY_ENABLED=alan ansible-inventory -i plugins/user_plugins_rel/foobar.ini --list --playbook-dir=plugins/user_plugins_rel/
```

You can avoid this unnecessary step with an auto plugin, which I will
develop a new example for on its own.
