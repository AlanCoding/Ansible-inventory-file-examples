### Ansible inventory cache

This tries to follow instructions in docs:

https://docs.ansible.com/ansible/latest/plugins/cache.html

with an eye toward eventual AWX enhancements in the inventory serialization.

```
ANSIBLE_INVENTORY_CACHE=True
ANSIBLE_INVENTORY_CACHE_PLUGIN=jsonfile
```

#### Plugins

Example of an inventory plugin that uses a cache.

https://github.com/ansible-collections/amazon.aws/blob/main/plugins/inventory/aws_ec2.py

Some key bits from that in the `parse` method.

```python
result_was_cached, results = self.get_cached_result(path, cache)

if not result_was_cached:
    results = self._query(regions, include_filters, exclude_filters, strict_permissions)

...

self.update_cached_result(path, cache, results)
```

```python
cache_key = self.get_cache_key(path)

self._cache[cache_key] = result
```

In the case of `aws_ec2` the `results` in question here is data specific to the source.

This is borrowed for the `alancoding.basic.only_cache` inventory plugin.
This plugin does nothing other than cache the current inventory state.
It does not add any inventory content.
It tries its best to always save to the cache, regardless of the settings.

We will see how that plugin interacts with the Ansible cache settings.

```
ansible-inventory -i changes.py -i only_cache.yml --list --export --playbook-dir=.
```

view docs of the inventory plugin

```
ANSIBLE_COLLECTIONS_PATH=collections/ ansible-doc -t inventory alancoding.basic.only_cache
```

We also have to support

```
ansible-inventory -i ../vault/single_var_file/inventory.ini -i only_cache.yml --list --export --playbook-dir=.
```

While that took some brutal debugging, it does, in fact, work.

#### Inventory script

To fully test this, we have an inventory script that has a side-effect.

```
rm side_effect.txt; ANSIBLE_INVENTORY_CACHE=True ANSIBLE_INVENTORY_CACHE_PLUGIN=jsonfile ansible-inventory -i changes.py --list --export
```

This DOES NOT WORK.

```
rm side_effect.txt; ANSIBLE_INVENTORY_CACHE=True ANSIBLE_INVENTORY_CACHE_PLUGIN=jsonfile ansible-playbook -i changes.py hello_world.yml
```

Does not work with playbook either. Why? Because the "script" inventory plugin
would have to have the caching machinery in it, and it doesn't.
