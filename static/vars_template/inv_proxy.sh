#!/bin/bash

ansible-inventory -i static/vars_template/inv -e my_variable=foobar --list
