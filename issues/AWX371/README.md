### Demo Problem for Smart Inventory hostvars Filtering

This folder contains example content to illustrate the problems with smart inventory.
This is primarily expressed in this issue:

https://github.com/ansible/awx/issues/371

A bullet-point summary of this (and other) smart inventory filtering issues is:

 - Smart inventory host_filter cannot express that a variable EQUALS a value, or do basic logic like NOT
 - Host/group/inventory variables cannot be filtered as a combined unit, as these are separate fields
 - Resultant smart inventories do not contain groups

We start out with the goal of contriving an example that reflects the complaints.
The first thing we do is create separate inventory _files_ that are assumed to
be imported into multiple inventories in AWX.
Sourcing hosts from multiple inventories is the entire point of smart inventory.
If you only needed to group/filter hosts in a single inventory, you would use a different tool.

Those two files are `east.ini` and `west.ini`.
These have common groups between them, so there is some different content.

#### Philosophy

The problems that we're going to solve come from multiple overlapping host _groupings_.
Without getting into the group hierarchy,
a sufficient and pure form of the problem is that we have mathematical sets of hosts.
Hosts can be divided into multiple, independent, mutually exclusive sets.

Abstractions are very hard to follow without some concrete basis.
So take Ansible inventory plugins for major cloud providers for a starting point.

https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html
https://docs.ansible.com/ansible/latest/collections/azure/azcollection/azure_rm_inventory.html
https://docs.ansible.com/ansible/latest/collections/google/cloud/gcp_compute_inventory.html

There is a large amount of experience with the schema from all these to establish
a number of common grouping patterns. Those are:

 - Machine state - running/stopped/shutting down/terminated
 - Region / sub-region / datacenter / further subdivisions
 - Account
 - Custom (special case) tags
   - an owner
   - purpose
   - team
 - Software details
   - AMI
   - operating system
 - production/staging/test/development split
 - network properties

It's common that cloud inventory sources use credentials _for an account_,
so one import is likely to be all of one single account.

It's also common that returned groups have no variables.

The fundamental goal with smart inventory is to query on a category that crosses
inventory boundaries.
We first have to set the inventory boundary - and in this case we do it by region.

Smart inventory's first-level problem is to return all hosts in an account over all regions.
Awkwardly, because `ansible-inventory` doesn't have a limit option, we use `ansible-playbook`.

```
ansible-playbook -i east.ini -i west.ini -i construct.yml --limit=account_1234 print_accounts.yml
```

This gives hosts from both source inventories (regions) in that account.

Now we need to consider how to get intersections of multiple overlapping criteria.

Academically, consider 3 types of groupings at the same time.
 - A/B/C for region
 - 1/2/3 for account
 - alpha/beta/gamma for state

To accomplish AND logic, we have to do this in a template.
Surprisingly, the `--limit` option will combing groups with OR, can NOT,
but cannot do AND combinations.

The mathematical objective is to intersect _some_ groups
but also _combine_ another grouping from the inventory source distinction.
So we combine two, like (3 & alpha). Putting into concrete terms, this is:

```
ansible-playbook -i east.ini -i west.ini -i construct.yml --limit=shutdown_in_product_dev print_accounts.yml
```

This only works because the constructed plugin does the work.
You could equally do the same kind of work via the `group_by` module.
Let's recap the 3 types of groupings.

 - region - done by producing literally different inventory files
 - state - done via a variable on the host in the source inventory
 - account - filtered by a group_vars/ vars plugin variable

The account is intended to be much more complicated.
The vars plugin hang off a lot of different properties,
and this is fairly realistic in the real world.
Those properties all correspond, as there is a real construct of an account in the real world.

The main work is done in the constructed plugin input.

```yaml
groups:
  shutdown_in_product_dev: resolved_state == "shutdown" and account_alias == "product_dev"
```

We have to add `use_vars_plugins: true` in this example, but would not in AWX
because inventory imports there do not distinguish between vars plugins.
However, you _would_ have to put that in if the `group_vars/` folder came
from the _playbook_ directory.
