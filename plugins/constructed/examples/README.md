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

#### Filter on

`source_vars`:

```yaml
plugin: constructed
strict: true
groups:
  is_shutdown: state | default("running") == "shutdown"
  product_dev: account_alias == "product_dev"
```

`limit`: `is_shutdown:&product_dev`

```yaml
plugin: constructed
strict: true
groups:
  shutdown_in_product_dev: state | default("running") == "shutdown" and account_alias == "product_dev"
```

`limit`: `shutdown_in_product_dev`

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
```

Establishment of goal:
