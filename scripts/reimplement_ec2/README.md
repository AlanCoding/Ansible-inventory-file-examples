## Re-Implementation of ec2.py

The script `ec2.py` is a supported inventory source for Ansible, which
will return an inventory containing the contents of Amazon Web Services
inventory.

https://github.com/ansible/ansible/blob/devel/contrib/inventory/ec2.py

This script is vendored along with Ansible Tower / AWX. It is also
a build-in inventory source, which is managed by Tower for you.

This folder shows how you can fully re-implement this inventory source
as a custom source from source control, including creating a custom
credential type to securely store the secrets needed to connect to AWS.

### Run the Example

You need tower-cli to run this.

https://github.com/ansible/tower-cli/

Additionally, you will need to modify the script to contain your
own personal private keys to AWS. After you have done that, you can
run the entire script by the command:

```
source scripts/environment/reimplement_ec2/tower_cli_setup.sh
```

When the script finishes, you can check your Tower / AWX server and you

