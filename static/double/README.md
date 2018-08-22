### Basic two file example

This is to use the `-i` flag multiple times.

```
ansible-inventory -i static/double/1.ini -i static/double/2.ini --list --export
```

Note that the file `2.ini` is not actually valid on its own.

The following command also fails:

```
ansible-inventory -i static/double/2.ini -i static/double/1.ini --list --export
```

The issue is that 2.ini defines vars for the "test" group.

```
[test:vars]
a=b
```

As of 2.7.0.dev0, the group "test" is still returned, and contains the
a=b variable.
