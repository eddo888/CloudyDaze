#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import re, os, sys, socket, paramiko

from Baubles.Logger import Logger
from Spanners.Squirrel import Squirrel
from Argumental.Argue import Argue
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config

for logger in ['boto','urllib3.connectionpool']:
		logging.getLogger(logger).setLevel(logging.ERROR)

logger = Logger()
squirrel = Squirrel()
args = Argue()

	
#___________________________________________________________________
@args.command(single=True)
class MySSH(object):

	@args.property(short='u')
	def username(self): return

	@args.property(short='H')
	def hostname(self): return
	
	@args.property(short='p')
	def password(self): return
	
	@args.property(short='P')
	def port(self): return
		
	@args.property(short='k', help='ssh key path')
	def key(self): return None
	
	@args.property(short='t', type=int, default=5, help='connect timeout seconds')
	def timeour(self): return None
	
	@args.property(short='v', flag=True, help='verbose logging')
	def verbose(self): return False

	def __init__(self):
		# force ip4 host connect
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.hostname, self.port))
		
		self.client = paramiko.SSHClient()		
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(
			paramiko.AutoAddPolicy()
		)
		
		if self.key:
			privateKey = paramiko.RSAKey.from_private_key_file(
				os.path.expanduser(self.key), 
				password=self.password
			)
			self.client.connect(
				self.hostname,
				sock=sock,
				port=self.port, 
				username=self.username,
				pkey=privateKey,
				timeout=self.timeout,
			)
		else:
			self.client.connect(
				self.hostname, 
				sock=sock,
				port=self.port, 
				username=self.username, 
				password=self.password, 
				timeout=self.timeout,
			)


	def __del__(self):
		self.close()
		

	def close(self):
		self.client.close()
		

	@args.operation
	@args.parameter(name='command', help='execute command string')
	def execute(self, command):
		print('$ %s' % command)
		stdin, stdout, stderr = self.client.exec_command(command)
		sys.stderr.write(stderr.read())
		return stdout.read()
		

#___________________________________________________________________
def main():
	username = 'ubuntu'
	hostname = 'pocketrocketsoftware.com'
	password = squirrel.get('ssh:%s:%s'%(username,hostname)) 
	key = '~/.ssh/id_rsa'
		
	remote = '/home/%s/hello.md' % username
	local = os.path.expanduser('~/Documents/hello.md')


	mySSH = MySSH(username, hostname, password=password, key=key)
	
	print(mySSH.execute('uptime'))
	mySSH.close()


#___________________________________________________________________
if __name__ == '__main__': main()

