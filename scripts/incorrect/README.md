### Why is the "no hostvars" example not right?

It is advisable that any modern Ansible dynamic inventory script should
return `hostvars` in its output. However, there is a supported legacy
method of returning host variables as well.

Say that you have a script `script.py` inside the current directory,
and it has inventory contents that include the host "foobar".
It is valid to have it behave as:

```
./script.py --list
{
  "foobars_group": ["foobar"]
}
```

Calling for foobar's variables:

```
./script.py --host foobar
{
  "foobars_variable": "value"
}
```

Ansible will call it with the 2nd pattern, because the 1st pattern of use
did not return the `_meta` key with `hostvars` inside of it.

_Some_ scripts may return the group/host content without any hostvars,
and also return that same content when called with `--host <hostname>`.
This is an incorrect hodgepodge of the 2 different standards, and is
not really correct in any way.

However, Ansible has no valid way of assessing that this is the situation.
So instead of causing an error, it returns a host list with the host
list repeated inside of the variables for all the hosts.

```
ansible-inventory -i scripts/incorrect/no_hostvars.py --list
{
    "_meta": {
        "hostvars": {
            "host1": {
                "group-1": [
                    "host1", 
                    "host2"
                ]
            }, 
            "host2": {
                "group-1": [
                    "host1", 
                    "host2"
                ]
            }
        }
    }, 
    "all": {
        "children": [
            "group-1", 
            "ungrouped"
        ]
    }, 
    "group-1": {
        "hosts": [
            "host1", 
            "host2"
        ]
    }, 
    "ungrouped": {}
}
```

The right answer for this case is "don't do that".
