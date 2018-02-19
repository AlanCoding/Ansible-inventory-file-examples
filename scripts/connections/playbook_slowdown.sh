
counter=0
while [ $counter -le 35 ]
do
  echo "running for $counter groups"
  # time NUMBER_GROUPS=$counter ansible-inventory -i ./scripts/connections/dag_max.py --list --export > /dev/null
  time NUMBER_GROUPS=$counter ansible-playbook -i ./scripts/connections/dag_max.py debugging/hello_world.yml > /dev/null
  ((counter++))
done


