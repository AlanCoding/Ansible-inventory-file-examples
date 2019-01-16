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


# assert that only one tempfile is visible
for tmpdir in ('/tmp', '/var/tmp'):
    files = readable_stuff(tmpdir)
    if files:
        errors.append(("Found temporary files", files))


# assert that no project directories are visible
lib_dir = '/var/lib'
if os.path.isdir(lib_dir):
    files = readable_stuff(lib_dir)
    if files:
        errors.append(("Found project directories", files))


# assert that no tower conf files are visible
etc_dir = '/etc'
if os.path.isdir(etc_dir):
    files = readable_stuff(etc_dir)
    if files:
        errors.append(("Tower config files", files))


# assert that no tower log files are visible
log_dir = '/var/log'
if os.path.isdir(log_dir):
    files = readable_stuff(log_dir)
    if files:
        errors.append(("Tower log files", files))


if errors:
    err_str = "The following errors were detected while running a proot-enabled inventory_update.\\n"
    for (name, files) in errors:
        err_str += "\\n# %s\\n" % name
        err_str += " - %s" % "\\n - ".join(files)
    raise Exception(err_str)


print json.dumps({})
