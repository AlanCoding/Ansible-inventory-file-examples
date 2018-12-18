### Azure inventory plugin

A valid set of environment variables to provide which fully specifies
auth are:

 - AZURE_SUBSCRIPTION_ID
 - AZURE_CLIENT_ID
 - AZURE_SECRET
 - AZURE_TENANT

The way the inventory file is formatted here requires auth to be
set via environment variables.

This needs the patch:

https://github.com/ansible/ansible/pull/50006

In order for it to work.

