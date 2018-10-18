### Issue reproduction

Just poke at the contents:

```
ansible-inventory -i issues/AWX1954/hosts.ini --list --export
```

To reproduce the issue:

```
ansible-playbook -i issues/AWX1954/hosts.ini issues/AWX1954/run.yml
```

Locally, this runs just fine.

