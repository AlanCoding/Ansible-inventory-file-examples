### Circular variable references

In the `foobar.py` inventory file, the host foobar has a variable foo which
has a value which is a pointer to the value.

This does not work with ordinary `ansible-inventory` because it serializes
it as JSON, however the `--yaml` flag will get it to work.

This will also work with playbooks (for better or worse).
