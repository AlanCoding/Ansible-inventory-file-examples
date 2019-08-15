### Source

Taken from

https://github.com/ansible/ansible/issues/31181

outputs are different:

1)

```
ansible-playbook -i issues/datetime/inventory.ini debugging/hostvars_print.yml
```


2)

```
./dump_and_read.sh issues/datetime/inventory.ini
ansible-playbook -i scripts/read_from_out.py debugging/hostvars_print.yml
```

The type is lost in the 2nd, turned into a string. It also prints differently.


