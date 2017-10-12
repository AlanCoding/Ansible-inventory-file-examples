# Create the default organization if it doesn't exist
tower-cli organization create --name="Default"

tower-cli project create --name="Ansible itself" --organization="Default" --scm-type="git" --scm-url="https://github.com/ansible/ansible.git" --wait

local_vars="{ansible_ssh_host: 127.0.0.1, ansible_connection: local}"

# --- Example of using protected environment variable ---
INPUTS="fields:
- id: username
  secret: false
  label: AWS access key
  type: string
- id: password
  secret: true
  label: AWS secret key
  type: string"

# We use a long multiline injector for the file
INJECTORS="env:
  AWS_ACCESS_KEY_ID: '{{ username }}'
  AWS_SECRET_ACCESS_KEY: '{{ password }}'
  EC2_INI_PATH: '{{ tower.filename }}'
file:
  template: |
    [ec2]
    regions = all
    regions_exclude = us-gov-west-1,cn-north-1
    destination_variable = public_dns_name
    vpc_destination_variable = ip_address
    route53 = False
    rds = False
    elasticache = False
    all_instances = False
    all_rds_instances = False
    include_rds_clusters = False
    all_elasticache_replication_groups = False
    all_elasticache_clusters = False
    all_elasticache_nodes = False
    cache_path = ~/.ansible/tmp
    cache_max_age = 0
    nested_groups = False
    replace_dash_in_groups = True
    expand_csv_tags = True
    group_by_instance_id = True
    group_by_region = True
    group_by_availability_zone = True
    group_by_ami_id = True
    group_by_instance_type = True
    group_by_key_pair = True
    group_by_vpc_id = True
    group_by_security_group = True
    group_by_tag_keys = True
    group_by_tag_none = True
    group_by_route53_names = True
    group_by_rds_engine = True
    group_by_rds_parameter_group = True
    group_by_elasticache_engine = True
    group_by_elasticache_cluster = True
    group_by_elasticache_parameter_group = True
    group_by_elasticache_replication_group = True
    [credentials]
    aws_access_key_id = {{ username }}
    aws_secret_access_key = {{ password }}"

tower-cli credential_type create --name="Re-implemented AWS" --inputs="$INPUTS" --injectors="$INJECTORS" --kind="cloud"

ACCESS_KEY=""
SECRET_KEY=""

tower-cli credential create --name="custom-defined AWS" --credential-type="Re-implemented AWS" --inputs="{username: $ACCESS_KEY, password: $SECRET_KEY}" --organization="Default"

tower-cli inventory create --name="SCM inventory AWS reimplemented" --variables="$local_vars" --organization="Default"
tower-cli inventory_source create --name="my AWS" --source="scm" --source-project="Ansible itself" --source-path="contrib/inventory/ec2.py" --inventory="SCM inventory AWS reimplemented" --credential="custom-defined AWS" --overwrite-vars=true
tower-cli inventory_source update "my AWS" --wait
