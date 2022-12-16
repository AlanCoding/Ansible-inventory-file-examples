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

Now, how does `ansible-inventory` compare in these cases?

```
time ansible-inventory -i create_10_hosts.ini --list --export --output=output.json  # 0.43 sec
time ansible-inventory -i create_100_hosts.ini --list --export --output=output.json  # 0.48 sec
time ansible-inventory -i create_1000_hosts.ini --list --export --output=output.json  # 0.8 sec
time ansible-inventory -i create_10000_hosts.ini --list --export --output=output.json  # 3.7 sec
```

This takes a long time at larger host counts.
The output file for the 10k hosts case is on the order of 300kb in size... not unexpected.
You can see that the `ansible-playbook` cases are able to create & destroy the hosts in faster time.
This is not due to the memory vs. disk distinction you might expect.

But what about the case of AWX? It takes inventory through a load-and-dump cycle.
How bad is it to re-use a previously dumped inventory?
To do this, we add a quick script to output the inventory.

```
time ansible-playbook -i dump_output.py -i test_host_01.destructed.yml --connection=local ping_once.yml  # 1.1 sec
```

Surprisingly! This does not take any more time before the dump-load cycle.
This suggests that the bottleneck in the process is ansible-inventory.
Let's check that. From:

```
time ansible-inventory -i create_10000_hosts.ini --list --export --output=output.json
```

We find that 1.77 sec of the total time was spent in generating the _python dict_ for the inventory.
That is, the `json_inventory` method in `ansible-inventory`.
Additionally, the `_play_prereqs` method takes 1.4 seconds.
This is surprising in the highest, since that's _more time_ that the entire `ansible-playbook`
run takes for this same inventory input.
Writing to a file only takes a measley 2 miliseconds.

#### Let's get a little silly

MOAR hosts!

```
time ansible-playbook -i create_100000_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 4.3 sec
time ansible-playbook -i create_1000000_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 4.5 min
```

What if we split it up and destruct every time??

```
time ansible-playbook -i split/split_1.ini -i test_host_01.destructed.yml --connection=local ping_once.yml  # 4.5 seconds
```

Now we start adding on more "split" inventories that will get all the hosts filtered out
 - -i split/split_2.ini -i test_host_01.destructed.yml --> 8.362 s
 - -i split/split_3.ini -i test_host_01.destructed.yml --> 12.4
 - -i split/split_4.ini -i test_host_01.destructed.yml --> 16.5
 - -i split/split_5.ini -i test_host_01.destructed.yml --> 21.7
 - -i split/split_6.ini -i test_host_01.destructed.yml --> 26.3
 - -i split/split_7.ini -i test_host_01.destructed.yml
 - -i split/split_8.ini -i test_host_01.destructed.yml
 - -i split/split_9.ini -i test_host_01.destructed.yml
 - -i split/split_10.ini -i test_host_01.destructed.yml

Going to the 5th split, you can see it keeping linearity, about 4 seconds per 100k hosts.
At about the 6th split, it may be losing linearity, but still unclear.

```
time ansible-playbook -i split/split_1.ini -i test_host_01.destructed.yml -i split/split_2.ini -i test_host_01.destructed.yml -i split/split_3.ini -i test_host_01.destructed.yml -i split/split_4.ini -i test_host_01.destructed.yml -i split/split_5.ini -i test_host_01.destructed.yml -i split/split_6.ini -i test_host_01.destructed.yml --connection=local ping_once.yml
```

what if we cut out the intermediate destructors?

```
time ansible-playbook -i split/split_1.ini -i split/split_2.ini -i split/split_3.ini -i split/split_4.ini -i split/split_5.ini -i split/split_6.ini -i test_host_01.destructed.yml --connection=local ping_once.yml
```

That gives a timing of 1 min 25 sec.
This shows that _the intermediate destructors help_.

#### Ansible inventory limit testing

https://github.com/ansible/ansible/pull/79596

```
time ansible-inventory -i create_10000_hosts.ini --list --export --output=output.json  # 4 sec Ansible devel / 10 sec limit branch
# rest of timings are from limit branch
time ansible-inventory -i create_10000_hosts.ini --list --export --limit=test_host_0 --output=output.json  # 2 sec
time ansible-inventory -i create_100000_hosts.ini --list --export --limit=test_host_0 --output=output.json  # 16.6 sec
time ansible-inventory -i split/split_1.ini --list --export --limit=test_host_0 --output=output.json  # 17.3 sec
time ansible-inventory -i split/split_1.ini -i split/split_2.ini --list --export --limit=test_host_0 --output=output.json  # 1 min 3 sec
time ansible-inventory -i split/split_1.ini -i test_host_01.destructed.yml -i split/split_2.ini --list --export --limit=test_host_0 --output=output.json --playbook-dir=.  # 51 sec
time ansible-inventory -i split/split_1.ini -i test_host_01.destructed.yml -i split/split_2.ini -i test_host_01.destructed.yml --list --export --limit=test_host_0 --output=output.json --playbook-dir=.  # 8 sec
```

#### Constructed

Adds the test host to new group "my_test_host".

```
ansible-inventory -i create_10_hosts.ini -i construct.yml --list --export
```

so let's repeat prior one, compare to 10 seconds.

```
time ansible-inventory -i create_10000_hosts.ini -i construct.yml --list --export --output=output.json  # 27 sec
time ansible-inventory -i create_10000_hosts.ini -i construct.yml --limit=test_host_0 --list --export --output=output.json  # 14 sec
```

None of this is particularly interesting.
