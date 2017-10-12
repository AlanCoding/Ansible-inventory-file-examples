### Environment Examples

These examples show the use of items specific to the environment where they
are ran. That means they will often fail if things are not set up in advance.

#### Run all examples with tower-cli

If you want to just see a demo of these examples, you can run the example
script, which will create all the needed environment-related resources
inside of Ansible Tower or AWX for you. This includes creating a project
from this repo and sourcing inventory from it.

```
pip install ansible-tower-cli
tower-cli config host <Tower host>
tower-cli config username <your username>
tower-cli config password <your password>
source scripts/environment/tower_cli_setup.sh
```

After you do this, you should be able to navigate to the 2 inventories created

 - SCM inventory env var example
 - SCM inventory file example

Within those, you should be able to see hosts that came from the encrypted
variables stored in their respective credentials.

#### env var script

The following command will show "foobar" as a host name, because it was read
from an environment variable by the script.

```
ENV_VAR=foobar ansible-inventory -i scripts/use_ENV_VAR.py --list
```

#### cwd script

This script shows you where you are (as a host).
It requires no setup in advance.

```
./scripts/environment/cwd.py 
```

#### Read from file

This example reads the filename `afile.txt` from the same directory the
script is in.

```
echo "foobar_file" > scripts/environment/afile.txt
./scripts/environment/file_local.py
ansible-inventory -i scripts/environment/file_local.py --list
```

You can see that `ansible-inventory` still works fine from that.

#### Read from env in conjunction with file

This example gets the filename's location from the environment variable.

```
echo "foobar_file" > scripts/environment/afile.txt
ENV_VAR=$(pwd)/scripts/environment/afile.txt ansible-inventory -i scripts/environment/file_from_env.py --list
```
