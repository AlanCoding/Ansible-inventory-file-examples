### Issue reproduction

Original issue report is in a comment in an issue in AWX:

https://github.com/ansible/awx/issues/1954#issuecomment-430459962

To reproduce the issue:

```
ansible-playbook -i issues/AWX1954/hosts.ini issues/AWX1954/playbook_dir/run.yml
```

Locally, this runs just fine.

#### Bug, as observed in AWX

Steps:

 - create an inventory that syncs `issues/AWX1954/hosts.ini`
 - create a JT that runs `issues/AWX1954/playbook_dir/run.yml`

#### Issue breakdown

The behavior seen in AWX is due to a combination of 2 different bugs
in Ansible core:

 - premature templating in the "is defined" check
 - failure to mark YAML variables as unsafe in JSON

##### Premature templating

```
ansible-playbook -i localhost, issues/AWX1954/premature_templating.yml
```

expected: debugs hello_world variable

```
PLAY [all] *****************************************************************************

TASK [debug] ***************************************************************************
ok: [localhost] => {
    "hello_world": "hello world!"
}

PLAY RECAP *****************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0
```

actual: errors with template error

```
PLAY [all] *****************************************************************************

TASK [debug] ***************************************************************************
fatal: [localhost]: FAILED! => {"msg": "The conditional check 'bad_syntax is defined' failed. The error was: An unhandled exception occurred while templating '{%NOTASTATEMENT%}'. Error was a <class 'ansible.errors.AnsibleError'>, original message: template error while templating string: Encountered unknown tag 'NOTASTATEMENT'.. String: {%NOTASTATEMENT%}\n\nThe error appears to have been in '/Users/alancoding/Documents/repos/ansible-inventory-file-examples/issues/AWX1954/premature_templating.yml': line 8, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n  tasks:\n    - debug:\n      ^ here\n"}
	to retry, use: --limit @/Users/alancoding/Documents/repos/ansible-inventory-file-examples/issues/AWX1954/premature_templating.retry

PLAY RECAP *****************************************************************************
localhost                  : ok=0    changed=0    unreachable=0    failed=1    skipped=0
```

##### Failure to mark JSON variables unsafe

This is simple to reproduce via:

```
ansible-inventory -i issues/AWX1954/hosts.ini --list --export
```

expected: host_vars and group_vars are marked unsafe.

```
host_var_unsafe: {
  "__ansible_unsafe": "{#NOTACOMMENT#}"
}
```

python reproduction of bug:

```
from ansible.parsing.ajson import AnsibleJSONEncoder
from ansible.parsing.yaml.loader import AnsibleLoader
import json

data = "host_var_unsafe: !unsafe '{#NOTACOMMENT#}'"
python_dict = AnsibleLoader(data).get_single_data()
print type(python_dict['host_var_unsafe'])
print json.dumps(python_dict, sort_keys=True, cls=AnsibleJSONEncoder)
```

This prints out:

```
{"host_var_unsafe": "{#NOTACOMMENT#}"}
```

The value of this variable is not marked unsafe.
