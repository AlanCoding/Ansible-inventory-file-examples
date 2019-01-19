### Linode partial example

This is an incomplete example for the linode inventory plugin.

Error types you may encounter:

 - you have Ansible < 2.8, so plugin not available
   - specifies unknown plugin 'linode'
 - you do not have the dependency installed
   - the Linode dynamic inventory plugin requires linode_api4.
 - you don't have auth specified
   - No setting was provided for required configuration plugin_type: inventory plugin: linode setting: access_token

```
ansible-inventory -i plugins/example_linode/linode.yml --list
```

The access_token can be provided as an env var, so hypothetically you could
use this file in a complete sense.

```
LINODE_ACCESS_TOKEN=foobar ansible-inventory -i plugins/example_linode/linode.yml --list
```

This has not been tested.
