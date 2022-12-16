#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import sys


with open('output.json', 'r') as f:
    shutil.copyfileobj(f, sys.stdout)
