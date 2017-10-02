### Vault examples

This has examples of using vault with inventory contents.

#### Can I use ansible-vault to encrypt host_vars and group_vars?

This is the case where variables are stored inside of a file.
It is replicated inside of the folder `vault/file_vars/` in this repo.
Examples of variables are stored inside the filename "encrypted" file
in the `group_vars` and `host_vars` folders.

The process of encrypting these is the following:

```
cp vault/file_vars/group_vars/unencrypted vault/file_vars/group_vars/raleigh

ansible-vault encrypt vault/file_vars/group_vars/raleigh
(put in password "password")

ansible-inventory -i vault/file_vars/inventory.ini --list --ask-vault-pass
(put in password "password")
```

#### Can I use that with vault-id?

Example for this is in `vault/vault_id` folder.

#### More References

https://gist.github.com/tristanfisher/e5a306144a637dc739e7

