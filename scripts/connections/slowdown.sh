
counter=0
while [ $counter -le 28 ]
do
  echo "running for $counter groups"
  time NUMBER_GROUPS=$counter ansible-inventory -i ./scripts/connections/dag_max.py --list --export > /dev/null
  ((counter++))
done


