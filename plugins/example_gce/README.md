### GCE inventory plugin

This use has been tested with a real server and seems to work

```
ansible-inventory -i example_gce/gcp.yml --list --export
```

There are multiple constraints that you need to adhere to for your own data
for instance, the private key must be formatted correctly.

It's unclear if any of the old environment variables are still effective,
testing seems to show that they are not. For example, setting `GCE_EMAIL`
as an environment variable cannot replace the need to specify
`service_account_email` in the inventory plugin file, and it also seems to
not overwrite the value if applied.

