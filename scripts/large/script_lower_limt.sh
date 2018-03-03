unset ANSIBLE_INVENTORY_PLUGINS
unset ANSIBLE_INVENTORY_ENABLED

# This tests to make sure that the script execution time itself
# isn't the bottleneck for the sizes involved

counter=0
while [ $counter -le 20 ]
do
  colin=':'
  justk='k'
  params=$counter$justk$colin$counter$justk$colin'1.0:'$conin'0.8'$colin'15'
  echo "params: $params"
  time INVENTORY_DIMENSIONS=$params ./scripts/large/large.py > /dev/null
  counter=$((counter + 1))
done


