### Vars precedence tests

This replicates some things said here:

https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#how-variables-are-merged

(cd into this folder before running things)

#### Basic Demo of Group Priority

```
ansible-inventory -i from_docs.yml --list --export
```

The inventory was modified to add a host "foohost" so we can see the precedence rules.
In order to actualize the variables on the host, you need to not use the `--export` flag.

```
ansible-inventory -i from_docs.yml --list
```

This shows `"testvar": "a"` in "foohost", demonstrating the intent of the example.

> In this example, if both groups have the same priority,
> the result would normally have been `testvar == b`,
> but since we are giving the `a_group` a higher priority the result will be `testvar == a`.

In this case, the `ansible_group_priority` variable comes from the "inventory source".

#### Inapplicability to group_vars

This repo hosts another example where the variable comes from the group_vars folder.
That lives in the `folder/` subfolder here.
Compared to the other example of `from_docs.yml`, it removes `ansible_group_priority`
from the `a_group` definition in `folder/modified.yml` add adds a file
in `folder/group_vars/a_group.yml` which sets the same `ansible_group_priority: 10`
variable on the same host.

```
ansible-inventory -i folder/modified.yml --list --export
```

Now get the resultant value, expecting that `ansible_group_priority` is ignored
according to the docs.

> `ansible_group_priority` can only be set in the inventory source and not in group_vars/,
> as the variable is used in the loading of group_vars.

```
ansible-inventory -i folder/modified.yml --list
```

As expected, we find `"testvar": "b"`, a reversion of the higher precedence.

#### Persistence Through Dumping-Loading Cycle

Firstly, this walks through the dumping-loading cycle for the group_vars example.
Dump the inventory:

```
ansible-inventory -i folder/modified.yml --list --export --output=folder/output.json
```

We can re-load the data dumped by a prior ansible-inventory command.
You can test this independent of the Ansible context by:

```
./folder/re_dump.py
```

This script does nothing more than print the output file to standard out.
This is necessary in order to get used as an Ansible script inventory,
which is the only format where the JSON data structure is recognized as an _input_.

Now, load this script inventory.

```
ansible-inventory -i folder/re_dump.py --list --export
```

And check the resultant value.

```
ansible-inventory -i folder/re_dump.py --list
```

This shows `"testvar": "a"`, which is different from the prior
section that showed direct use of the group_vars (the `folder/`) example.

In other words, the process of loading and dumping loses the context of
where a variable comes from, and in this case, changing the behavior.

This is expected to be encountered by any use of such an inventory source in AWX.
Create an SCM inventory source from this repo using `folder/modified.yml`
as the source path and then run a job against it.

It should encounter the same behavior (`testvar` being a, not b)
because AWX, itself, implements a dumping-loading cycle with the `--export`
flag as a basic component of its inventory system.
