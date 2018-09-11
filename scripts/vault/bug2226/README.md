### Bug 2226 reproduction

See links:

https://github.com/ansible/awx/issues/2226

https://github.com/aldobongio/awx-bug-2226

Reproduction here:

```
ansible-playbook debugging/hostvars_print.yml -i scripts/vault/bug2226/single.py --ask-vault-pass
```

Issue is that the hostvar "baz" retains the encrypted content, and does not
decrypt. Other similar uses of Ansible vault will decrypt.

Files in this folder:

 - `awx.py` - the inventory script endpoint output from the awx-bug-2226 repo steps
 - `single.py` - a reduced set of reproduction steps only using single list


