#!/usr/bin/env python
import os
import json
import re


errors = list()
my_file = __file__
my_dir = os.path.dirname(my_file)
my_filename = my_file.rsplit(os.path.sep, 1)[1]


# assert that only one tempfile is visible
for tmpdir in ('/tmp', '/var/tmp'):
    for files in os.listdir(tmpdir):
        matches = [f for f in files if f != my_filename]
        if matches:
            files = map(lambda f: os.path.join(tmpdir, f), files)
            errors.append(("Found temporary files", files))


# assert that no project directories are visible
lib_dir = '/var/lib'
if os.path.isdir(lib_dir):
    files = os.listdir(lib_dir)
    if files:
        errors.append(("Found project directories", files))


# assert that no tower conf files are visible
etc_dir = '/etc'
if os.path.isdir(etc_dir):
    files = os.listdir(etc_dir)
    if files:
        errors.append(("Tower config files", files))


# assert that no tower log files are visible
log_dir = '/var/log'
if os.path.isdir(log_dir):
    files = os.listdir(log_dir)
    if files:
        errors.append(("Tower log files", files))


if errors:
    err_str = "The following errors were detected while running a proot-enabled inventory_update.\\n"
    for (name, files) in errors:
        err_str += "\\n# %s\\n" % name
        err_str += " - %s" % "\\n - ".join(files)
    raise Exception(err_str)


print json.dumps({})
