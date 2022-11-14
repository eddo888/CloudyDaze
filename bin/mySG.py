#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, os, re

if os.path.dirname(sys.argv[0]) == '.':
	sys.path.append('..')

from CloudyDaze.MySG import args

args.execute()

