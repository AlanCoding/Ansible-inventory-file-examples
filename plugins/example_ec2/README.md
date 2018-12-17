### EC2 inventory plugin

The file `aws_ec2.yml` is a bare-bones inventory plugin file,
assuming that the important parameters will be passed via environment
variables.

This is fairly simple use described well in the documentation:

https://docs.ansible.com/ansible/2.7/plugins/inventory/aws_ec2.html

Usage:

```
AWS_ACCESS_KEY_ID=<your_id> AWS_SECRET_ACCESS_KEY=<your_key> ansible-inventory -i plugins/example_ec2/aws_ec2.yml --list --export
```

