## AWX constructed inventory feature examples

These are organized by the structure of the input inventories.

### Group name and variables filtering

Inventory Content Description:
Two hetrogenous of conditions are demonstrated here.
The hosts inside that inventory can be thought of as a Venn Diagram.
It contains several hosts such that some will fit one condition, the other condition,
neither, or both. This results in 4 hosts in total for demonstration purposes.
 - First condition is that the `state` variable defined on the host is set to "shutdown"
 - Second condition is membership in a group with `account_alias` variable set to "product_dev"

Inventory Definition:
This folder defines the inventory as an ini type at `two_conditions.ini`.

```ini
[account_1234]
host1
host2 state=shutdown

[account_4321]
host3
host4 state=shutdown

[account_1234:vars]
account_alias=product_dev

[account_4321:vars]
account_alias=sustaining
```

Establishment of goal:
We want to return only hosts that are present in the group with the
account_alias variable of "product_dev".
There are 2 approaches to this. The first one here is better.

#### Construct 2 groups, limit to intersection

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  is_shutdown: state | default("running") == "shutdown"
  product_dev: account_alias == "product_dev"
```

`limit`: `is_shutdown:&product_dev`

This constructed inventory input creates a group for both of the categories
and uses the `limit` (host pattern) to only return hosts that are in the
intersection of those two groups.

#### Construct 1 group, limit to group

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  shutdown_in_product_dev: state | default("running") == "shutdown" and account_alias == "product_dev"
```

`limit`: `shutdown_in_product_dev`

This input creates one group that only includes host that match both criteria.
The limit is then just the group name by itself, returning only 1 host,
same as the other approach.

### Nested groups

Inventory Content Description:
Two groups exists where one is a child of the other.
The child group has a host inside of it, and the parent group has a variable defined.
Due to how Ansible core works, the parent group's variable will be available in
hostvars as a playbook is running, and can be used for filtering.

Inventory Definition:
The best way to visualize this is with the yaml format at `nested.yml`

```yaml
all:
  children:
    groupA:
      children:
        groupB:
          hosts:
            host1: {}
      vars:
        filter_var: filter_val
    ungrouped:
      hosts:
        host2: {}
```

Establishment of goal:
Filter hosts based on a variable from a group they are an indirect member of.
This is accomplished by treating that variable the same as any other hostvar.

#### Filter on nested group name

`source_vars`: empty

`limit`: `groupA`

#### Filter on nested group property

In the inventory contents, you can see that `host2` is not expected to have
the variable `filter_var` defined, because it is not in any of the groups.
Because of using `strict: true`, we need to use a default value so that
hosts without that variable defined, like `host2`, will return `False`
from the expression, as opposed to throwing an error.

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  filter_var_is_filter_val: filter_var | default("") == "filter_val"
```

`limit`: `filter_var_is_filter_val`

### Ansible facts

Inventory Definition:
It is hard to give a specification for the inventory for Ansible facts,
because to populate the system facts you need to run a playbook against
the inventory that has `gather_facts: true`.
The actual facts will differ system-to-system.

#### Example problem - filtering on env var

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  hosts_using_xterm: ansible_env.ANSIBLE_STDOUT_CALLBACK == "xterm"
```

`limit`: `hosts_using_xterm`

#### Example problem - hosts by processor type

Or as another example, filtering Intel hosts

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  intel_hosts: "GenuineIntel" in ansible_processor
```

`limit`: `intel_hosts`
