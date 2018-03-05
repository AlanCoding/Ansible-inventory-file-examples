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
delimiter. This is implemented in `scripts/large/large.py`, taking
those parameters as an environment variable.

```
<hosts>:<groups>:<host-group>:<group-group>:<Nvars>:<len>
# shorthand
<Nh>:<Ng>:<nhg>:<ngg>:<nvars>:<len>
# example setting the variable
export INVENTORY_DIMENSIONS=10k:500:2.0:2.0:5:50
```

### Scaling different metrics demos

##### Large host number

![over 9000!](vegeta.jpeg?raw=true)

```
time INVENTORY_DIMENSIONS=10k:0:0.0:0.0:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

6 seconds to run

##### Large group number

```
time INVENTORY_DIMENSIONS=0:10k:0.0:0.0:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

3 seconds to run

##### Groups and hosts only

Here, let's play around with a large number of groups and hosts, where no
group-group connections exist. Firstly, we try without any of the hosts
being members of the groups.

```
time INVENTORY_DIMENSIONS=5k:5k:0.0:0.0:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

4 seconds to run

Now, let's keep the total number of "things" the same, but make all hosts
members of 2 groups each. To do this, we're reducing the number of hosts
and groups, because we're adding 5k group-host memberships.
By that, we're doing 2.5k hosts + 5k memberships + 2.5k groups = 10k things.

```
time INVENTORY_DIMENSIONS=2.5k:2.5k:2.0:0.0:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

2.5 seconds to run

##### Groups tree only

Next, let's do group-group connections. We're not using the 10k number here,
because it would never finish. This is a reproduction of the issue


```
time INVENTORY_DIMENSIONS=0:25:0.0:12.0:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

27 seconds to run

##### Hosts, groups, and shallow tree

This is trying to be more realistic about what a real large inventory
should look like.
1k hosts + 1k groups + 3k host-group + 3k group-group = 8k things
for `INVENTORY_DIMENSIONS=1k:1k:3.0:3.0:2:15`, but that's too much.
The group-group membership was decreased until this ran.

```
DEBUG=true INVENTORY_DIMENSIONS=1k:1k:3.0:2.5:2:15 ./scripts/large/large.py
time INVENTORY_DIMENSIONS=1k:1k:3.0:2.5:2:15 ansible-playbook -i scripts/large/large.py debugging/hello_world.yml
```

about 10 seconds to run

This example provides some preliminary evidence that the complaints related
to large inventory performance is primarily a consequence of the group
tree scaling issues.


#### Profile a large inventory

```bash
INVENTORY_DIMENSIONS=2k:2k:1.0:0.8:2:15 python -m cProfile -o outme $(which ansible-playbook) -i scripts/large/large.py debugging/hello_world.yml
pyprof2calltree -i outme
qcachegrind outme.log
```

Probably a better example is the complex example from above.

```
INVENTORY_DIMENSIONS=1k:1k:3.0:2.5:2:15 python -m cProfile -o outme $(which ansible-playbook) -i scripts/large/large.py debugging/hello_world.yml
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

### Possibilities for Speedup

Options that need to be considered for their impact on speed:
 - disable `_groups_dict_cache`
 - rewrite the plugin to do a multi-pass building
 - change Host `add_group` to only loop over direct parents in recursion

