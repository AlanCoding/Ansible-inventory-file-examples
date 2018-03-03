### Programatically generated large inventories

How to specify a large inventory?

 - number of hosts
 - number of groups
 - rough number of
   - group-group connections per group
   - host-group connections per host
 - number of variables per group/host
 - data size of each vars chunk

Need some way to specify this, easiest with a single env var but a
delimiter.

```
<hosts>:<groups>:<host-group>:<group-group>:<Nvars>:<len>
```

Example:

```
export INVENTORY_DIMENSIONS=10k:500:2.0:2.0:5:50
```

#### Profile a large inventory

```bash
INVENTORY_DIMENSIONS=2k:2k:1.0:0.8:2:15 python -m cProfile -o outme $(which ansible-playbook) -i scripts/large/large.py debugging/hello_world.yml
pyprof2calltree -i outme
qcachegrind outme.log
```

#### Small demo

smaller example...

```
INVENTORY_DIMENSIONS=7:5:0.8:0.8:1:15 ./scripts/large/large.py
```

now, run `ansible-inventory`:

```
# As ansible-inventory
INVENTORY_DIMENSIONS=7:5:0.8:0.8:1:15 ansible-inventory -i scripts/large/large.py --list --export
# As debug playbook (note that task only runs once)
INVENTORY_DIMENSIONS=7:5:0.8:0.8:1:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

Debug info on that

 - hosts 7
 - groups 5
 - host-group connections - 5.6 predicted, 6 actual
 - group-group connections - 3.2 predicted, 3 actual

Note that since the connection ratios are both under 1 than some "orphaned"
objects exist. That means that some hosts in in the `ungrouped` group and
some groups and children of the `all` group.

#### Scaling tests

##### Script Execution Time

First we have to make sure that the script, itself, isn't taking
forever to run.

```
source scripts/large/script_lower_limt.sh
```

Last testing done showed that this could run in 0.5 seconds for 20k
of both hosts and groups (with as many connections of each).

