### Performance Problems

https://github.com/ansible/ansible/pull/13673

```
python -m cProfile -o outme /Users/meyers/ansible/ansible/bin/ansible-playbook -i inventory main.yml >> stdout
pyprof2calltree -i outme
qcachegrind outme.log
```

Particular target of interest for shipping out an issue in Ansible repo

26 groups puts the ansible-playbook call into the 1.5 min range.
27 gets 3 min

```
time NUMBER_GROUPS=26 ansible-playbook -i ./scripts/connections/dag_max.py debugging/hello_world.yml
```

