### Host ordering issue

> awx uses wrong host from group (host ordering is inconsistent)

https://github.com/ansible/awx/issues/2240

This folder should accumulate some inputs that express that issue.

```
ansible-inventory -i three.ini --list --export
```

This shows:

```json
"other_order": {
    "hosts": [
        "node01",
        "node02",
        "node03"
    ]
}
```

compare with inventory source definition

```ini
[other_order]
node02
node01
node03
```

This reflects that the ordering of hosts inside of a group is done by a name sort.
That is consistent with the Ansible core logic in `ansible-inventory`.

```python
for h in sorted(group.hosts, key=attrgetter('name')):
```

https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/inventory.py#L353

However, this does not guarentee consistency with `ansible-playbook`.
So we have to use a playbook to test that.

```
ansible-playbook listing_playbook.yml -i three.ini --limit=docker[0]
```

This consistently targets `node01`.

```
ansible-playbook listing_playbook.yml -i three_reversed.ini --limit=docker[0]
```

This consistently targets `node03`, highlighting that `ansible-inventory` is wrong.
