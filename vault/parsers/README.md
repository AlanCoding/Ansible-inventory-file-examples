### Ansible external vars processors

There is a need for external libraries to interact with Ansible, and sometimes
these libraries will need to process variables that contain "special"
keywords or types that need to be processed specially.

This folder contains examples of modifying the python JSON and YAML libraries
to work with native Ansible data, so that the result of reading and
dumping them will behave consistently with how Ansible core behaves.

#### Links

https://github.com/ansible/ansible/pull/45924

(rejected) https://github.com/ansible/ansible/pull/45514

https://gist.github.com/sivel/2513c72d83c5b23a77c6fb400e9739cd

