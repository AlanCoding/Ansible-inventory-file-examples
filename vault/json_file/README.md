### JSON Encryption hostvars vs. extra_vars

This folder tests that use of JSON-based encrypted values will properly
extend to use in `--extra-vars` in `ansible-playbook` runs.

#### Generating secret

I generated two secrets for this example and encrypted them both

 - id: alan_host, content: hostz, var name: host_secret
 - id: alan_ev, content: extra_varz, var name: vars_secret

Encrypted by the following CLI commands, on the prompt, the password
"password" was provided in both cases. The format provided here is what
I will refer to as the "constructor" format.

```
ansible-vault encrypt_string "hostz" --name=host_secret --vault-id=alan_host@prompt
New vault password (alan_host): 
Confirm vew vault password (alan_host): 
host_secret: !vault |
          $ANSIBLE_VAULT;1.2;AES256;alan_host
          35356666616633303337313766346562613961313262333530663432393965303736653334306433
          6239666265343936343462653836386162343234353961330a306665396665353364613863316362
          66646663313737393763383565333237316663666339623063646666646261643338616261633330
          3634313634666264620a383632386661653330326435633861333031643334643237366430313733
          3733
Encryption successful
ansible-vault encrypt_string "extra_varz" --name=vars_secret --vault-id=alan_ev@prompt
New vault password (alan_ev): 
Confirm vew vault password (alan_ev): 
vars_secret: !vault |
          $ANSIBLE_VAULT;1.2;AES256;alan_ev
          33626665646161613531376438336635373834366433383537623562336166643363633530346235
          3136653363663330313437326434383739666162623336330a623433316366346465336163333238
          36383931626361623230336662613238366566666230643732313366353838333231326138393463
          6662373163326436330a633436386332356638353865663736616563326666663466623633373161
          6333
Encryption successful
```

This is converted into the new form by removing the YAML constructor,
and replacing with the new JSON-targeted syntax.

This is what I will refer to as the "funky" format.

```
host_secret:
    __ansible_vault: |
        $ANSIBLE_VAULT;1.2;AES256;alan_host
        35356666616633303337313766346562613961313262333530663432393965303736653334306433
        6239666265343936343462653836386162343234353961330a306665396665353364613863316362
        66646663313737393763383565333237316663666339623063646666646261643338616261633330
        3634313634666264620a383632386661653330326435633861333031643334643237366430313733
        3733
vars_secret:
    __ansible_vault: |
        $ANSIBLE_VAULT;1.2;AES256;alan_ev
        33626665646161613531376438336635373834366433383537623562336166643363633530346235
        3136653363663330313437326434383739666162623336330a623433316366346465336163333238
        36383931626361623230336662613238366566666230643732313366353838333231326138393463
        6662373163326436330a633436386332356638353865663736616563326666663466623633373161
        6333
```

Now these are saved in various places in this directory so that the
inventory and playbook commands below will pick things up.

Note that the inventory command does not take extra_vars, so `vars_secret` is
only surfaced in the playbook command. It also does not perform decryption.

```
ansible-inventory -i vault/json_file/inventory.ini --list --export
ansible-playbook debugging/hostvars_print.yml -i vault/json_file/inventory.ini --vault-id=alan_host@prompt --vault-id=alan_ev@prompt
```

Formats and places and outcomes (as of Sept 2018):

 - `vars_secret_funky_json`: decrypts
 - `vars_secret_funky`: does not
 - `vars_secret_constructor`: decrypts
 - `inventory_file_secret_funky`: decrypts
 - `host_secret_funky`: does not
 - `host_secret_constructor`: decrypts
 - `host_secret_funky_json`: decrypts

So in short, the "funky" format is not supported inside of YAML right now.
