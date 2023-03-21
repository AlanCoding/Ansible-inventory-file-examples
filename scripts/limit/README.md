### Testing for Ansible inventory limit

This is a feature in Ansible core 2.15


```
ansible-inventory -i scripts/limit/nested.py --list --export
```

returns both hosts

```
ansible-inventory -i scripts/limit/nested.py --list --export --limit=groupA
```

returns only `host1`

It is also help to apply the environment variable

```
ANSIBLE_HOST_PATTERN_MISMATCH=error
```

With that, bad limits like the following will error

```
ANSIBLE_HOST_PATTERN_MISMATCH=error ansible-inventory -i scripts/limit/nested.py --list --export --limit=groupefe
```
