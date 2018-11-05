### Tower authentication specification

Scenario: I have some tooling, how should it accept username / password
to an instance of AWX or Ansible Tower?

Great question!

Let's gather together all the examples here of how clients tend to do this.

The file must be named specifically `tower_inventory.yml`, and this
folder contains an example.

```
plugin: tower
host: your_tower_server_network_address
username: your_username
password: your_password
inventory_id: the_ID_of_targeted_inventory
verify_ssl: True/False
```


