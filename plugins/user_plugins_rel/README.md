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

Very important: the inventory _plugin_ had to be manually specified here by name.
The relevant Ansible setting (`enable_plugins` in the config file) is a comma
separated list of names of plugins to allow use of. However, the folder
in the _plugin search paths_ where the "alan" plugin can be found
was picked up implicitly from the playbook directory. This is how you
can use custom plugins without juggling absolute paths, and as far as I know,
this is the only way to do it.

You can avoid the unnecessary step of specifying the enabled plugins
with an auto plugin, which I will develop a new example for on its own.
