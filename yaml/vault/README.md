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

#### Group vars

from issue, both fail to decrypt

https://github.com/ansible/ansible/issues/32160

```
# failed to decrypt
ansible-inventory -i yaml/vault/groupvar_foo.yml --vault-password-file=yaml/vault/bar --list
# doesn't try to decrypt
ansible-inventory -i yaml/vault/groupvar_foo.yml --vault-password-file=yaml/vault/bar --list --yaml
# failed to decrypt
ansible-playbook -i yaml/vault/groupvar_foo.yml --vault-password-file=yaml/vault/bar debugging/hostvars_print.yml -vvv
```

```
# cannot serialize
ansible-inventory -i yaml/vault/groupvar_artemis.yml --vault-id=alan@scripts/vault/passwords/password --list
# doesn't try to decrypt
ansible-inventory -i yaml/vault/groupvar_artemis.yml --vault-id=alan@scripts/vault/passwords/password --list --yaml
# success decrypting, shows in hostvars
ansible-playbook -i yaml/vault/groupvar_artemis.yml --vault-id=alan@scripts/vault/passwords/password debugging/hostvars_print.yml -vvv
```

