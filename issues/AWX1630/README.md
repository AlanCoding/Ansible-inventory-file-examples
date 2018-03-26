### Vault passwords from 2 different sources

In order to demonstrate the cfg example, you have to cd to this directory.

```
cd issues/AWX1630/
ansible-inventory -i inventory.ini --list
# alt
ansible-playbook ../../debugging/hostvars_print.yml -i inventory.ini 
```

This correctly decrypts.

Also provide the vault id through prompting at the same time

```
ansible-playbook ../../debugging/hostvars_print.yml -i inventory.ini --vault-id=alan@prompt
```

This also works if the correct vault password is provided.
It still works if the _wrong_ vault password is provided.

#### Reproducing the actual issue

The expectation is that a _missing_ vault password (perhaps in the 
.gitignore) will not block decryption via the prompts.
It does.

```
rm password
ansible-playbook ../../debugging/hostvars_print.yml -i inventory.ini --vault-id=alan@prompt
Vault password (alan): 
ERROR! The vault password file /Users/alancoding/Documents/repos/ansible-inventory-file-examples/issues/AWX1630/password was not found
```

