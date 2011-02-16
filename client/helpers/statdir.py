#!/usr/bin/env python

def getProperty(configFile, section, prop):
	try:
		import configparser
		config = configparser.ConfigParser()

		config.read(configFile)

		return config[section][prop]

	except KeyError:
		print ('Configuration file does not exist, or is corrupted. Please create it using helpers/makeconfig.py');
		return ''

syncpath = getProperty('../config.ini', 'config', 'syncpath')

import os
import os.path
print (syncpath)
print (os.stat(syncpath))
# Check for st_atime
