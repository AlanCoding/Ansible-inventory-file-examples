### The "destructed" inventory plugin

This is a cheekily named inventory plugin which removes host.
The name is inspired by the "constructed" inventory plugin in Ansible core.

```
ansible-inventory -i example.ini -i destructed.yml --list --export --playbook-dir=.
```

This only returns "host1" because that's the only thing that matched the pattern.
That is defined inside of `destructed.yml`:

```yaml
plugin: alancoding.basic.destructed
host_pattern: host1
```
