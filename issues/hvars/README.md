### Hostvars processing behavior

This folder contains examples of partial and full implementations of the
`_meta` and `hostvars` keys inside of an inventory source. The scripts
implement the following behaviors with the corresponding results.

 - not providing `_meta`: script is re-called for the hosts
 - not providing `hostvars`: script is re-called for the hosts
 - not providing the host name in hostvars: hostvars are empty
 - providing one name in hostvars but not another: missing hostvars are empty
 - providing empty hostvars: hostvars are empty