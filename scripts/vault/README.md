### Ansible Vault Re-Dumper Development

I don't want to decrypt Ansible vault content.

I don't want to encrypt Ansible vault content.

I just don't want errors to be thrown with vault content.
I want to say "decrypt later", and I want to manage the content,
just pass it through, right now.

#### Setting up the secret

This is route repetition of official docs.
This section exists in order to detail the exact steps to reproduce.

Vault credential details:

 - id: "alan"
 - password: "password"
 - contents: "artemis", with or without a trailing return

http://docs.ansible.com/ansible/2.4/vault.html

```
ansible-vault encrypt_string --vault-id alan@scripts/vault/passwords/password 'artemis\n' --name 'should_be_artemis_here'
should_be_artemis_here: !vault |
          $ANSIBLE_VAULT;1.2;AES256;alan
          33343133656536356166303131613166626361303662396435326663613636336561636533396138
          3636626133333136313935376362326462363862316230660a646363393535366430333033336131
          35333237616137383462626232656639386265316239643634663134383265646532623463633662
          6435343233666431360a323466616465366439343963333839396538386431646163353763333762
          6131
Encryption successful
```

This is manually forced into an inventory file, as so:

```
_meta:
  hostvars:
    foobar:
        should_be_artemis_here: !vault |
            $ANSIBLE_VAULT;1.2;AES256;alan
            33343133656536356166303131613166626361303662396435326663613636336561636533396138
            3636626133333136313935376362326462363862316230660a646363393535366430333033336131
            35333237616137383462626232656639386265316239643634663134383265646532623463633662
            6435343233666431360a323466616465366439343963333839396538386431646163353763333762
            6131
ungrouped:
  hosts:
  - foobar
```

Actual encrypted value may vary by example.

#### The initial CLI demo

```bash
ansible-playbook -i scripts/vault/bypass_constructor.py --vault-id=alan@scripts/vault/passwords/password debugging/hostvars_print.yml
```

This shows the vaulted secret inside of its output.

```
        "should_be_artemis_here": "artemis\n"
```

#### Basic re-dumping example

The challenge is to be able to algorithmically provide vaulted content
inside of other inventory contents.

```bash
ansible-playbook -i scripts/vault/awx_redumper.py --vault-id=alan@scripts/vault/passwords/password debugging/hostvars_print.yml
```

This example gets `ansible-inventory` to decrypt vaulted contents that a
script outputted.

