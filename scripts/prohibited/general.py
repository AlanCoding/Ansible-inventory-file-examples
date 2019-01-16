#!/usr/bin/env python
import os
import json
import re


errors = list()
my_file = __file__
my_dir = os.path.dirname(my_file)
my_filename = my_file.rsplit(os.path.sep, 1)[1]


def readable_stuff(dir):
    found = []
    for file in os.listdir(dir):
        abs_path = os.path.join(dir, file)
        if os.path.isdir(abs_path):
            try:
                os.listdir(abs_path)
                found.append(file)
            except (OSError, IOError):
                pass
        else:
            try:
                with open(abs_path, 'r') as f:
                    f.read()
                found.append(file)
            except (OSError, IOError):
                pass
    return found


errors = {}


# assert that only one tempfile is visible
for tmpdir in ('/tmp', '/var/tmp'):
    files = readable_stuff(tmpdir)
    if files:
        errors.setdefault('tmp', []).extend(files)


# assert that no project directories are visible
lib_dir = '/var/lib'
if os.path.isdir(lib_dir):
    files = readable_stuff(lib_dir)
    if files:
        errors['var'] = files


# assert that no tower conf files are visible
etc_dir = '/etc'
if os.path.isdir(etc_dir):
    files = readable_stuff(etc_dir)
    if files:
        errors['etc'] = files


# assert that no tower log files are visible
log_dir = '/var/log'
if os.path.isdir(log_dir):
    files = readable_stuff(log_dir)
    if files:
        errors['log'] = files


if errors:
    print("The following errors were detected while running a proot-enabled inventory_update.\\n")
    raise Exception(json.dumps(errors, indent=2))


print json.dumps({})
