import re, os, sys, socket, paramiko

from Baubles.Logger import Logger
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config
from CloudyDaze.MySCP import MySCP, args


print(args.execute())
