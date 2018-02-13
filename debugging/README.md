### Debugging

This folder contains some Ansible _playbooks_ to use to compare the
`ansible-playbook` behavior to the `ansible-inventory` behavior,
which is expected to be identical.

#### Surprising empty groups behavior

The following files will define a group that is empty:
 - scripts/var_files/just_host.py
 - scripts/empty_group.py

These should be used as the inventory file for running the example
`add_host_and_echo.yml` as follows.

```
ansible-playbook -i {inventory file} debugging/add_host_and_echo.yml
```

The surprising outcome is that the second set of print statements detect
the group vars (inside hostvars), whereas the first
print statements before the addition of the new host contains no trace
of the group.

Even more surprising is the fact that the `empty_group.py` shows the empty
group (`barfoo`) in the group list before the host add, whereas the
second one does not.

The behavior here has several issues
 - Ansible should show groups that come from variable plugins when the
   variable `groups` is referenced
 - `ansible-inventory` should show the variables on groups

The first issue can be replicated simply by comparing the output of the
following two commands.

```
ansible-inventory -i scripts/empty_group.py --list
ansible-inventory -i scripts/var_files/just_host.py --list
```

The first command shows the empty group, but the second command does not.

Why this is a problem:

credit to reference: 

https://github.com/chrismeyersfsu/test-awx-job/commit/a32753bff0ca600bc886157f1fe53a98f3afc699

The point of `ansible-inventory` is to produce the same behavior as `ansible-playbook`.
This is violated in cases where `add_host` is used when the inventory contains
empty groups created by vars plugins.

An established example of this is the following.

```
ansible-inventory -i ./inventory/partial --list > partial_generated
# Test case A
ansible-playbook -i echo.sh playbooks/minimal_add_host.yml
# Test case B
ansible-playbook -i ./inventory/partial playbooks/minimal_add_host.yml
```

Here, the original source inventory is `./inventory/partial`. However, we
can see that the representation that `ansible-inventory` creates of this
inventory is incomplete. This leads to test case A yielding different
results from test case B.
