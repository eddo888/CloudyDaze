#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import sys, re, os, json, logging, requests, urllib, boto.ec2

from collections import namedtuple

from Baubles.Logger import Logger
from Argumental.Argue import Argue

from MyAWS import config

logger = Logger()
args = Argue()

	
#_____________________________________________________
@args.command(single=True)
class MySG(object):

	@args.property(short='s', default='sg-0fd6edded8cc6d9cd')
	def security_group(self): return

	@args.property(short='r', default='ap-southeast-2')
	def aws_region(self): return
	
	@args.property(short='p', default='Stibo')
	def aws_profile(self): return

	@args.property(short='u', default='https://api.ipify.org?format=json')
	def url(self): return
	
	@args.property(short='c')
	def callback(self): return
	
	@args.property(short='v', flag=True, help='verbose logging')
	def verbose(self): return False

	ports = {
		22: 'tcp',
		443: 'tcp',
		3389: 'tcp',
		1521: 'tcp',
		8888: 'tcp',
	}
	
	types=[
		'tcp',
		'udp',
		'icmp',
		-1
	]

	#_________________________________________________
	def __init__(self):
		self.config = config()

		if self.verbose:
			logger.setLevel(logging.DEBUG)
		else:
			logger.setLevel(logging.INFO)

		if self.config:
			self.conn = boto.ec2.connect_to_region(
				self.aws_region,
				aws_access_key_id=self.config['Stibo']['aws_access_key_id'],
				aws_secret_access_key=self.config['Stibo']['aws_secret_access_key'],
			)
		else:
			self.conn = boto.ec2.connect_to_region(
				self.aws_region,
				profile_name=self.aws_profile,
			)
			

	#_________________________________________________
	def __del__(self):
		self.conn.close()


	#_________________________________________________
	def __callback(self, deltas):
		if self.callback:
			import webbrowser
			url = self.callback + '?argv=' + urllib.quote(json.dumps(deltas))
			logger.debug(url)
			webbrowser.open(url)
		else:
			# pythonista only
			pass

	
	#_________________________________________________
	def dictate(self, d):
		return d['cidr_ip'].split('/')[0]


	#_________________________________________________
	@args.operation
	def myip(self):
		results = requests.get(self.url).json()
		_ip = results['ip']
		logger.debug('myip = %s'%_ip)
		return _ip


	#_________________________________________________
	def __security_group(self):
		for sg in self.conn.get_all_security_groups():
			if sg.id != self.security_group: continue
			logger.debug('sg = %s'% sg)
			return sg


	#_________________________________________________
	@args.operation
	def granted(self):
		_granted = list()
		sg = self.__security_group()
		for rule in sg.rules:
			for grant in rule.grants:
				_grant = dict(
					ip_protocol=str(rule.ip_protocol),
					cidr_ip=str(grant),
					from_port=int(rule.from_port),
					to_port=int(rule.to_port),
				)
				logger.debug('authorised = %s'%self.dictate(_grant))
				_granted.append(_grant)
				ip = str(grant).replace('/32','')
		return _granted
	

	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	def enable(self, ips=[]):
		if len(ips) == 0:
			ips = [self.myip()]
		sg = self.__security_group()

		_granted = self.granted()
		_enabled = []
		_todo = list()

		# create list of grants to do
		for ip in ips:
			for port, tipe in self.ports.items():
				if tipe not in self.types:
					sys.stderr.write('%s not in %s\n'%(tipe,self.types))
					continue
				_do = dict(
					ip_protocol=tipe,
					from_port=port,
					to_port=port,
					cidr_ip='%s/32'%ip,
				)
				logger.debug('todo = %s'%self.dictate(_do))
				_todo.append(_do)
		
		# filter out already completed grants
		for _grant in _granted:
			for t in range(len(_todo))[::-1]:
				_do = _todo[t]
				test = map(lambda x: _do[x] == _grant[x], _grant.keys())
				if all(test):
					logger.debug('authorised = %s'%self.dictate(_do))
					_enabled.append(_do)
					del _todo[t]

		# process the remaing todo items
		for _do in _todo:
			logger.debug('authorising = %s'%self.dictate(_do))
			_enabled.append(_do)
			sg.authorize(src_group=None,**_do)
			
		self.__callback(dict(enabled=_enabled))
		return _enabled


	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	@args.parameter(name='forall', short='a', flag=True, help='revoke all')
	def revoke(self, ips=[], forall=False):
		if len(ips) == 0:
			ips = [self.myip()]
		sg = self.__security_group()
		_granted = self.granted()
		_revoked = []
		for ip in ips:
			for _grant in _granted:
				if forall or ip == _grant['cidr_ip'].split('/')[0]:
					_revoked.append(_grant)
					logger.debug('revoking = %s'%self.dictate(_grant))
					sg.revoke(
						ip_protocol=_grant['ip_protocol'],
						from_port=_grant['from_port'],
						to_port=_grant['to_port'],
						cidr_ip=_grant['cidr_ip'],
						src_group=None
					)
		
		self.__callback(dict(revoked=_revoked))
		return _revoked
	

	#_________________________________________________
	@args.operation
	@args.parameter(name='ips', nargs='*', short='i')
	@args.parameter(name='forall', short='a', flag=True, help='revoke all')
	def replace(self, ips=[], forall=False):
		result = dict()
		result['revoked'] = self.revoke(ips, forall)
		result['enabled'] = self.enable(ips)
		return result
		
		
#_____________________________________________________
def main():	
	#print('sys.argv: %s'%json.dumps(sys.argv))
	argv = sys.argv[1:]
	
	try:
		if 'x-callback-url' in sys.argv[-1]:
			callback = sys.argv[-1]
			argv = list(['-c', callback]) + list(sys.argv[1:-1])
		else:
			# from pythonista libraries
			import editor
			# fix for pythonista tools icons
			if sys.argv[-1] == editor.get_path():
				argv = sys.argv[1:-1]
	except:
		pass
		
	#print('argv: %s'%json.dumps(argv))	
	args.parse(argv)	
	results = args.execute()
	print(json.dumps(results, indent=4))
	
	
#_____________________________________________________
if __name__ == '__main__': main()

