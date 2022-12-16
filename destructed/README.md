### The "destructed" inventory plugin

This is a cheekily named inventory plugin which removes host.
The name is inspired by the "constructed" inventory plugin in Ansible core.

```
ansible-inventory -i example.ini -i destructed.yml --list --export --playbook-dir=.
```

This only returns "host1" because that's the only thing that matched the pattern.
That is defined inside of `destructed.yml`:

```yaml
plugin: alancoding.basic.destructed
host_pattern: host1
```

#### Playbook scale testing

If you pass 10k hosts into virtually any Ansible CLI command, it is likely
to take a very very long time. We want to be sure that the destructed
inventory plugin resolves those concerns. So some commands are given here.

To test this, we are using the `ping_once.yml` playbook.
Regardless of how many hosts are in the inventory, this will just run once.
As you can verify, it still takes a long time to run the playbook if you have a large inventory.

```
ansible-playbook -i create_10_hosts.ini --connection=local ping_once.yml  # approx 1 sec
ansible-playbook -i create_100_hosts.ini --connection=local ping_once.yml  # approx 1.8 sec
ansible-playbook -i create_1000_hosts.ini --connection=local ping_once.yml  # approx 11.5 sec
ansible-playbook -i create_10000_hosts.ini --connection=local ping_once.yml  # I gave up
```

Compare to where we make use of `--limit`

```
time ansible-playbook -i create_10_hosts.ini --connection=local --limit=test_host_0 ping_once.yml  # 0.8 sec
time ansible-playbook -i create_100_hosts.ini --connection=local --limit=test_host_0 ping_once.yml  # 0.8 sec
time ansible-playbook -i create_1000_hosts.ini --connection=local --limit=test_host_0 ping_once.yml  # 0.9 sec
time ansible-playbook -i create_10000_hosts.ini --connection=local --limit=test_host_0 ping_once.yml  # 2.2 sec
```

Can we get the same performance with the `destructed` inventory plugin?

```
time ansible-playbook -i create_10_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 0.8 sec
time ansible-playbook -i create_100_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 0.8 sec
time ansible-playbook -i create_1000_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 0.87 sec
time ansible-playbook -i create_10000_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 1.1 sec
```

Yes. We get the same performance.

We learned some important things here.
Importantly, you really DO NOT want to pass in a bunch of hosts into `ansible-playbook`
if you do not intend to automate against them, because that will destroy performance.
