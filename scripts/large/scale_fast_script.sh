export ANSIBLE_INVENTORY_PLUGINS=$(PWD)/plugins/user_plugins/
export ANSIBLE_INVENTORY_ENABLED=fast_script


counter=0
while [ $counter -le 4 ]
do
  colin=':'
  justk='k'
  params=$counter$justk$colin$counter$justk$colin'1.0:'$conin'0.8'$colin'2'$colin'15'
  echo "INVENTORY_DIMENSIONS=$params"
  time INVENTORY_DIMENSIONS=$params ansible-playbook -i scripts/large/large.py debugging/hello_world.yml > /dev/null
  counter=$((counter + 1))
done


unset ANSIBLE_INVENTORY_PLUGINS
unset ANSIBLE_INVENTORY_ENABLED