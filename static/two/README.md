### Two hosts, demos of host_vars

This demos vars plugins in the situation where multiple inventories are involved.
The final result:

```
ansible-inventory -i static/two/inv1/inventory1.ini -i static/two/inv2/inventory2.ini --list --export
```

This shows variables defined in `inv2/host_vars` for all 3 hosts. To visualize...

```
static/two/
├── inv1
│   └── inventory1.ini
├── inv2
│   ├── host_vars
│   │   ├── host1
│   │   ├── host2
│   │   └── host3
│   └── inventory2.ini
└── README.md
```

Note that `host1` is unique to inventory 1, and `host3` is unique to inventory 2.
Thus, backing up, we find that this does not contain the `host1` variable.

```
ansible-inventory -i static/two/inv1/inventory1.ini --list --export
```

However, from the first command, using both inventories, we get:

```
"host3": {
    "var_host3": "foo3"
}
```

This is a non-obvious result which this is documenting.

Hosts can obtain vars from vars plugins in different inventories.
