#!/usr/bin/env python3

# from python libraries
import sys, re, os, uuid, json, logging, urllib
from time import sleep

# from AWS API libraries
import boto
import boto.ec2
import boto.ec2.elb

from Baubles.Logger import Logger
from Perdy.pretty import prettyPrintLn, Style

from CloudyDaze.MyAWS import config

logger = Logger()

logging.getLogger('boto').setLevel(logging.WARNING)

# http://boto.readthedocs.org/en/latest/ec2_tut.html
	
#_________________________________________________
class MyEC2(object):

	def __init__(self):
		aws_profile = 'default'
		self.config = config()
		self.conn = boto.ec2.connect_to_region(
			self.config[aws_profile]['region'],
			aws_access_key_id=self.config['default']['aws_access_key_id'],
			aws_secret_access_key=self.config['default']['aws_secret_access_key'],
		)

		
	def __del__(self):
		self.close()
		
	def close(self):
		self.conn.close()
		
	def list(self,ids):
		if type(ids) == str:
			ids = [ids]
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				if len(ids) > 0 and instance.id not in ids: continue
				#print(json.dumps(dir(instance),indent=4))
				#print(instance.ip_address)
				status[str(instance.id)] = str(instance.state)
		return status
		
	def start(self,ids):
		if type(ids) == str:
			ids = [ids]
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				logger.info(instance)
				if len(ids) > 0 and instance.id not in ids: continue
				if instance.state not in [ u'pending', u'starting', u'running' ]:
					instance.start()
					logger.info(instance)
				status[str(instance.id)] = str(instance.state)
		return status
		
	def stop(self,ids):
		if type(ids) == str:
			ids = [ids]
		status = dict()
		for reservation in self.conn.get_all_reservations():
			logger.debug('reservation: %s'%reservation.id)
			for instance in reservation.instances:
				logger.info(instance)
				if len(ids) > 0 and instance.id not in ids: continue
				if instance.state not in [ u'pending', u'stopping', u'stopped' ]:
					instance.stop()
					logger.info(instance)
				status[str(instance.id)] = str(instance.state)
		return status
		
#_________________________________________________
def main():
	output = ''
	
	#print('sys.argv: %s'%json.dumps(sys.argv))
	try:
		# from pythonista libraries
		import editor
		# fix for pythonista tools icons
		if sys.argv[-1] == editor.get_path():
			argv = sys.argv[1:-1]
		else:
			argv = sys.argv[1:]
		logger.debug('argv: %s'%json.dumps(argv))
	except:
		argv = sys.argv[1:]
	
	#print(argv)
	
	if '://' in argv[-1]:
		callback = argv[-1]
		del argv[-1]
	else:
		callback = None
		
	if len(argv) == 0:
		output = dict(usage='<list,stop,start> [ids,..]')
	else:
		myEC2 = MyEC2()
		if len(argv) >= 2:
			ids = argv[1:]
		else:
			ids = list()
		if argv[0] == 'list':
			output = myEC2.list(ids)
		if argv[0] == 'start':
			output = myEC2.start(ids)
		if argv[0] == 'stop':
			output = myEC2.stop(ids)
			
	print(json.dumps(output,indent=4))

	import webbrowser
	if callback:
		url = '%s?argv=%s'%(callback, urllib.quote(json.dumps(output)))
		#print(url)
		webbrowser.open(url)
	
			
#_________________________________________________
if __name__ == '__main__': main()
