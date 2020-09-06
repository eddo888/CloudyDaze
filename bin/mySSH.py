#!/usr/bin/env python3

import re, os, sys, socket, paramiko

from Baubles.Logger import Logger
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config
from CloudyDaze.MySSH import MySSH, args


print(args.execute())
