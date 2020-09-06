#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import re, os, sys, socket, paramiko

sys.path.append('..')

from Baubles.Logger import Logger
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config
from CloudyDaze.MySCP import MySCP, args


print(args.execute())
