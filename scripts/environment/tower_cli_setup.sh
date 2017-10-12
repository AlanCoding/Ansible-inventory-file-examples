# Create the default organization if it doesn't exist
tower-cli organization create --name="Default"

# Create a project that points to this repo, this gives us access to all the
# files in this directory, which we pass as --source-path creating
# the inventory source later on
tower-cli project create --name="Inventory file examples" --organization="Default" --scm-type="git" --scm-url="https://github.com/AlanCoding/Ansible-inventory-file-examples.git" --wait

# The host this creates isn't real, these inventory vars
# make sure we don't actually try to connect
local_vars="{ansible_host: 127.0.0.1, ansible_connection: local}"

# --- Example of using protected environment variable ---

# These define the use input to the credential, and their encrypted state
INPUTS="fields:
- id: ENV_VAR
  secret: true
  label: An environment variable
  type: string"

# This contains instructions to save the input as an environment variable
INJECTORS="env:
  ENV_VAR: '{{ ENV_VAR }}'"

# Template for the credential that can contain secret data
tower-cli credential_type create --name="Single Env Var" --inputs="$INPUTS" --injectors="$INJECTORS" --kind="cloud"

# Actual instantiation of the credential, with ENV_VAR potentially being secret
tower-cli credential create --name="encrypted env var" --credential-type="Single Env Var" --inputs="ENV_VAR: my_tower_cli_example" --organization="Default"

# Create the inventory, which holds the sources, groups, and hosts
tower-cli inventory create --name="SCM inventory env var example" --variables="$local_vars" --organization="Default"
# Create the inventory source
tower-cli inventory_source create --name="env var file" --source=scm --source-project="Inventory file examples" --source-path="scripts/environment/use_ENV_VAR.py" --inventory="SCM inventory env var example" --credential="encrypted env var" --overwrite-vars=true
# sync the inventory source - this creates the hosts
tower-cli inventory_source update "env var file" --wait


# --- Example of using protected contents inside a file ---
INPUTS="fields:
- id: secret_host
  secret: true
  label: The name of the host to fill in
  type: string"

INJECTORS="env:
  ENV_VAR: '{{ tower.filename }}'
file:
  template: '{{ secret_host }}'"

tower-cli credential_type create --name="File and env var" --inputs="$INPUTS" --injectors="$INJECTORS" --kind="cloud"

tower-cli credential create --name="File encrypted var" --credential-type="File and env var" --inputs="secret_host: my_tower_cli_example2" --organization="Default"

tower-cli inventory create --name="SCM inventory file example" --variables="$local_vars" --organization="Default"
tower-cli inventory_source create --name="secret file var" --source=scm --source-project="Inventory file examples" --source-path="scripts/environment/file_from_env.py" --inventory="SCM inventory file example" --credential="File encrypted var" --overwrite-vars=true
tower-cli inventory_source update "secret file var" --wait
