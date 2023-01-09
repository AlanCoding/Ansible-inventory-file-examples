#!/bin/bash

trap "exit" INT

rm -rf *.time

echo "***************************************************************************"
echo "Running ansible-playbook with run_once=true"
echo ""

host_scales=(10 100 1000 10000 100000 1000000)

twrap="timeout 30 time -o run_once.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-playbook -i create_${host_count}_hosts.ini --connection=local ping_once.yml"
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done

echo ""
echo ""
echo "***************************************************************************"
echo "Running ansible-playbook with --limit to only select a single host"
echo ""

twrap="timeout 30 time -o playbook_limit.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-playbook -i create_${host_count}_hosts.ini --connection=local --limit=test_host_0 ping_once.yml"
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done

echo ""
echo ""
echo "***************************************************************************"
echo "Running ansible-playbook with destructed inventory plugin to limit to a single host"
echo ""

twrap="timeout 30 time -o playbook_destructed.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-playbook -i create_${host_count}_hosts.ini -i test_host_01.destructed.yml --connection=local ping_once.yml"
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done

echo ""
echo ""
echo "***************************************************************************"
echo "Running ansible-inventory against the specified inventory"
echo ""

twrap="timeout 30 time -o inventory.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-inventory -i create_${host_count}_hosts.ini --list --export --output=output.json"
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done

echo ""
echo ""
echo "***************************************************************************"
echo "Running ansible-inventory with the destructed inventory plugin"
echo ""

twrap="timeout 30 time -o inventory_destructed.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-inventory -i create_${host_count}_hosts.ini -i test_host_01.destructed.yml --list --export --output=output.json --playbook-dir=."
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done

echo ""
echo ""
echo "***************************************************************************"
echo "Running ansible-inventory with --limit to limit to one host"
echo ""

twrap="timeout 30 time -o inventory_limit.time -a"

for host_count in "${host_scales[@]}"
do
  echo ""
  echo ""
  ansible_command="ansible-inventory -i create_${host_count}_hosts.ini --list --export --limit=test_host_0 --output=output.json"
  echo $ansible_command
  $twrap $ansible_command
  echo "return code of command: $?"
done
