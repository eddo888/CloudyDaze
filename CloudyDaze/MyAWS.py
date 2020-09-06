#!/usr/bin/env python3

import os

from configparser import ConfigParser

#___________________________________________________________________
def config():
	dot_aws = os.path.expanduser('~/Documents/.aws/credentials')
	#os.environ['AWS_SHARED_CREDENTIALS_FILE'] = dot_aws

	if not os.path.exists(dot_aws): return
	
	parser = ConfigParser()
	parser.read(dot_aws)
	
	_config = dict.fromkeys(parser.sections())
	for key in _config.keys():
		_config[key] = dict()
		for (name,value) in parser.items(key):
			_config[key][name] = value
		
	#json.dump(_config,sys.stdout,indent=4)
	
	return _config


#___________________________________________________________________
def main():
	print(config())


#___________________________________________________________________
if __name__ == '__main__': main()
