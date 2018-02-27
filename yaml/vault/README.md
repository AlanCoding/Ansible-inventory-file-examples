### YAML vault is special in Ansible

When does `ansible-inventory` pass through vault content, and when does it not?

```
# Does not pass it through (error)
ansible-inventory -i yaml/vault/hostvar_artemis.yml --list
# Passes it through
ansible-inventory -i yaml/vault/hostvar_artemis.yml --list --yaml
```

Other sources of vault variables can be dumped as YAML without decrypting.

```
# file vars - Does not pass it through
ansible-inventory -i vault/file_vars/inventory.ini --list --yaml
# script vars - Does pass it through
ansible-inventory -i scripts/vault/awx_redumper.py --list --yaml
```
