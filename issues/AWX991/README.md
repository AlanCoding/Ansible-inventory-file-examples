### Insufficiency of JSON ansible-inventory output

Consider the two use cases ran from the root of this project.

```
# case for JSON
ansible-inventory -i issues/AWX991/inv --list
# case for YAML
ansible-inventory -i issues/AWX991/inv --list --yaml
```

The keys for the JSON case are strings even though the original type
of these keys were integers.
