#!/bin/bash

ansible-inventory -i "$1" --list --export > out

OUTPUT="$(ansible-inventory -i scripts/read_from_out.py --list --export)"

ORIG="$(cat out)"

if [ "$OUTPUT" == "$ORIG" ]
then
  echo "Source $1 is reversible."
else
  echo "Source $1 cannot be run multiple times with same result."
fi
