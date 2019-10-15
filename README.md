# Ansible-inventory-file-examples
Examples and counter-examples of Ansible inventory files

Goals of these are mostly academic, to demonstrate a syntax, scaling pattern,
or issue reproducer. None of these are designed to reflect best practices
for using Ansible.

README files are given in many subdirectories.

Top level is mostly organized by file type, with further subdivisions
by topic. While this isn't always maintained, an attempt is made.

#### Using these

Everything is designed to be ran from the CLI from the root of the project
root. Aside from one folder for playbook, and other testing scripts,
everything is an inventory file that goes in with the `-i` flag.
That means you should see `-i <relative path in project>`. There are
multiple testing commands you can use on any given inventory file.

```
# run the absolute minimal playbook
ansible-playbook -i top_level_file.ini debugging/hello_world.yml
# print the hostvars for all the hosts
ansible-playbook -i top_level_file.ini debugging/hostvars_print.yml
# dump standard representation of the inventory contents
ansible-inventory -i top_level_file.ini --list --export
```

#### Quick and dirty performance profiling

Reference for doing the cProfile stuff

https://github.com/ansible/ansible/pull/13673

```bash
pip install pyprof2calltree
```

```bash
python -m cProfile -o outme $(which ansible-playbook) -i <rel_path> debugging/hello_world.yml
pyprof2calltree -i outme
qcachegrind outme.log
```

### Commands from the root of project

#### Ansible config file example

Inventory plugin path via magic `inventory_plugins` dir:

```
ansible-inventory -i plugins/config_path/same_dir/cow.yaml --playbook-dir=plugins/config_path/same_dir --list
```

Inventory plugin path via child directories:

```
ansible-inventory -i plugins/config_path/sub_dir/cow.yaml --playbook-dir=plugins/config_path/sub_dir/child_dir --list
```

Inventory plugin path via relative directory and using parent directories:

```
ansible-inventory -i plugins/config_path/inventory_dir/cow.yaml --playbook-dir=plugins/config_path/other_dir --list
```

All of these work testing locally.

