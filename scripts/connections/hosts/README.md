### Host-Group maxing out connections

This folder contains examples that have the same DAG in group structure
as its parent directory. However, it also adds hosts to the mix, making
those hosts members of the groups in the DAG.

In all cases, every host is either a direct or indirect member of
every group.

In all cases, the number of total "things" is also minimized.

In all cases, the severity of the problem (given a limited number of "things")
is maximized.

This typically means that

```
(number of group edges) = approx (number of hosts)
```

It was found that doing direct membership of every host to every group
was impractical due to Nh*Ng scaling. It was possible for dag_max
due to Nh*sqrt(Ng) scaling, but still maybe not a good idea.

A switch was made to only connect all hosts to the one group at the end
of the stack, which is easily identifiable in both cases.
This switch can be turned off by setting `ALL_GROUPS=true`, but
if you do this with 10k hosts, you are asking for trouble.

#### Use

Instead of specifying the NUMBER_GROUPS, we specify NUMBER_HOSTS here.
The number of groups is generated automatically.

```
NUMBER_HOSTS=10 ./scripts/connections/hosts/dag_max.py
NUMBER_HOSTS=10 ansible-inventory -i ./scripts/connections/hosts/dag_max.py --list --export
```

#### Script performance

We can't have the majority of the time taken to run Ansible just get
consumed by the script itself. Due diligence dictates that we test this.
Again, 10k hosts is our standard reference.

```
time NUMBER_HOSTS=10000 ./scripts/connections/hosts/dag_max.py > /dev/null
real	0m0.047s
user	0m0.027s
sys	0m0.017s

time NUMBER_HOSTS=10000 ALL_GROUPS=true ./scripts/connections/hosts/dag_max.py > /dev/null
real	0m0.241s
user	0m0.174s
sys	0m0.062s

time NUMBER_HOSTS=10000 ./scripts/connections/hosts/dag_linear.py > /dev/null
real	0m0.084s
user	0m0.060s
sys	0m0.020s
```

#### Ansible performance

The reason I did this was because I knew how the source code of the inventory
loader for Ansible was structured. There is an extremely heavy penalty
for a large amount of indirect host-group membership.

##### pre-fix

```
# ouch
time NUMBER_HOSTS=250 ansible-playbook -i ./scripts/connections/hosts/dag_max.py debugging/hello_world.yml
real	0m7.033s
user	0m6.726s
sys	0m0.284s

# oof
time NUMBER_HOSTS=90 ALL_GROUPS=true ansible-playbook -i ./scripts/connections/hosts/dag_max.py debugging/hello_world.yml
real	0m7.668s
user	0m7.277s
sys	0m0.325s

# maybe ok-ish?
time NUMBER_HOSTS=900 ansible-playbook -i ./scripts/connections/hosts/dag_linear.py debugging/hello_world.yml
real	0m6.196s
user	0m5.837s
sys	0m0.331s
```


##### post-fix

```
time NUMBER_HOSTS=10000 ansible-playbook -i ./scripts/connections/hosts/dag_max.py debugging/hello_world.yml
real	0m9.059s
user	0m7.974s
sys	0m1.130s

# Input memberships scale with Nh*sqrt(2*Ng) > 100k, so maybe this isn't terrible
time NUMBER_HOSTS=2000 ALL_GROUPS=true ansible-playbook -i ./scripts/connections/hosts/dag_max.py debugging/hello_world.yml
real	0m14.346s
user	0m13.766s
sys	0m0.468s

# Not great for this case still (maximum indirect membership)
# performance here not really improved in any meaningful sense
time NUMBER_HOSTS=1000 ansible-playbook -i ./scripts/connections/hosts/dag_linear.py debugging/hello_world.yml
real	0m7.793s
user	0m7.408s
sys	0m0.337s
```


