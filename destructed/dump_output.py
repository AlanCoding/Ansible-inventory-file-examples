#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
import sys


with open('output.json', 'r') as f:
    shutil.copyfileobj(f, sys.stdout)
