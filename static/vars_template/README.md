### Templating and Ansible CLI Interplay

Initial "it works on my machine" example:

```
ansible-playbook debugging/hostvars_print.yml -i static/vars_template/inv -e my_variable=foobar
```

out of the output, you can find:

```
"alan_var": "Templated from extra var foobar",
```

```
"print_this": "variable with my var foobar"
```

These are two different means of templating a variable.

#### ansible-inventory

Ideally, we believe we should be able to replicate any `ansible-playbook -i` behavior
by first using `ansible-inventory`, saving the ouptut, and patching that
into a new `ansible-playbook` run.
In practice, this is challenging is many subtle ways.

Reconstructing the prior example for the `ansible-inventory` stage:

```
ansible-inventory -i static/vars_template/inv -e my_variable=foobar --list
```

This does not template anything.

#### Using in Conjunction

This feeds ansible-inventory output to ansible-playbook.

```
ansible-playbook debugging/hostvars_print.yml -i static/vars_template/inv_proxy.sh -e my_variable=foobar
```

This will correctly substitute in the templated values again.
