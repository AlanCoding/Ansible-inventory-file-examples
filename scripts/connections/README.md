### Performance Problems

Dense group structures (`scripts/connections/dag_max.py`) have extremely
poor performance. Proof:

```
time NUMBER_GROUPS=26 ansible-playbook -i scripts/connections/dag_max.py debugging/hello_world.yml > /dev/null
 [WARNING]: Could not match supplied host pattern, ignoring: all
 [WARNING]: provided hosts list is empty, only localhost is available

real	1m33.101s
user	1m31.590s
sys	0m0.765s
```

Running `ansible-inventory` is about 100 times slower for this type of
inventory, but it does't matter very much, only changing the cutoff from
around 21 to 27.

Linear group structures (`scripts/connections/dag_linear.py`) do not have the
same poor performance, this is true even when the number of edges is the
same. Proof:

```
time NUMBER_GROUPS=500 ansible-playbook -i scripts/connections/dag_linear.py debugging/hello_world.yml > /dev/null 
 [WARNING]: Could not match supplied host pattern, ignoring: all
 [WARNING]: provided hosts list is empty, only localhost is available

real	0m2.231s
user	0m1.918s
sys	0m0.289s
```

#### Profiling

Reference for doing the cProfile stuff

https://github.com/ansible/ansible/pull/13673

```
NUMBER_GROUPS=26 python -m cProfile -o outme $(which ansible-playbook) -i ./scripts/connections/dag_max.py debugging/hello_world.yml
pyprof2calltree -i outme
qcachegrind outme.log
```

Particular target of interest for shipping out an issue in Ansible repo

26 groups puts the ansible-playbook call into the 1.5 min range.
27 gets 3 min

#### Group structures for reference

```
NUMBER_GROUPS=15 ansible-inventory -i scripts/connections/dag_max.py --graph
(yields extremely large output for some reason)
```

```
NUMBER_GROUPS=15 ansible-inventory -i scripts/connections/dag_linear.py --graph
@all:
  |--@g14:
  |  |--@g13:
  |  |  |--@g12:
  |  |  |  |--@g11:
  |  |  |  |  |--@g10:
  |  |  |  |  |  |--@g9:
  |  |  |  |  |  |  |--@g8:
  |  |  |  |  |  |  |  |--@g7:
  |  |  |  |  |  |  |  |  |--@g6:
  |  |  |  |  |  |  |  |  |  |--@g5:
  |  |  |  |  |  |  |  |  |  |  |--@g4:
  |  |  |  |  |  |  |  |  |  |  |  |--@g3:
  |  |  |  |  |  |  |  |  |  |  |  |  |--@g2:
  |  |  |  |  |  |  |  |  |  |  |  |  |  |--@g1:
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |--@g0:
  |--@ungrouped:
```

