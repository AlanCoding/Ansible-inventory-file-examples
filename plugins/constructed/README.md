### Constructed plugin inventory modification

The inventory `constructed.yml` is not an inventory in itself.

Instead, it modifies the inventory that has already been set up by the
inventory sources listed before it.

The file `inv_contents.ini` have been created to meet the expectations of
the constructed file. You pass both in the form of:

```
ansible-inventory -i plugins/constructed/inv_content.ini -i plugins/constructed/constructed.yml --list --export
```



