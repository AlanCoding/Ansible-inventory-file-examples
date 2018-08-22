### Basic two file example

This is to use the `-i` flag multiple times.

```
ansible-inventory -i static/double/1.ini -i static/double/2.ini --list --export
```

Note that the file `2.ini` is not actually valid on its own.