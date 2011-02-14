#!/usr/bin/env python

# The client
#   Copyright (C) 2011 Thomas Gummerer
#
# This file is part of Filesync.
# 
# Filesync is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Filesync is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Filesync.  If not, see <http://www.gnu.org/licenses/>. 

# TODO Move methods below to another class or at least file
def getProperty(configFile, section, prop):
	try:
		import configparser
		config = configparser.ConfigParser()

		config.read(configFile)

		return config[section][prop]

	except KeyError:
		print ('Configuration file does not exist, or is corrupted. Please create it using helpers/makeconfig.py');
		return ''

def isInConfig(configFile, section):
	try:
		import configparser
		config = configparser.ConfigParser()

		config.read(configFile)
		
		return (section in config)
		
	except KeyError:
		print ('Configuration file does not exist, or is corrupted. Please create it using helpers/makeconfig.py');
		return ''

###############################################################################

# Path to configuration file
configFile = 'config.ini'

# Method to get the syncronization path
# getSyncPath(configFile)
import connection
con = connection.Connection(getProperty(configFile, 'config', 'serveraddress'))

# Credentials not in the config file, ask the user for them and write them to config file
if (not(isInConfig(configFile, 'userdata'))):
	import configparser
	config = configparser.ConfigParser()
	config.read(configFile)
	config['userdata'] = {}
	config['userdata']['username'] = input("Username: ")
	# Know this should not be done, but I don't like to write more than one line for it
	config['userdata']['password'] = hashlib.sha1(getpass.getpass("Password: ").encode("utf8")).hexdigest()

	with open('config.ini', 'w') as configfile:
		config.write(configfile)
	
	
# Get the credentials from the config file
username = getProperty(configFile, 'userdata', 'username')
password = getProperty(configFile, 'userdata', 'password')

# TODO Give the user a chance to correct the credentials
con.send(bytes("0 " + username, "utf8"))
if (con.recieve().decode("utf8") == 1):
	print ("Username is wrong. Please edit it in the config.ini file.")
	con.close()
	exit()


con.send(bytes("1 " + password, "utf8"))
if (con.recieve().decode("utf8") == 1):
	print ("Wrong password. Please change it in the config.ini file.")
	con.close()
	exit()

import sync
syncdir = getProperty(configFile, 'config', 'syncpath')
sy = sync.Sync(syncdir, con)
while True:
	text = input("Type 'sync' to synchronize the sync folder, 'exit' to exit: ")
	if (text == 'sync'):
		sy.sync()
	elif (text == 'exit'):
		break

# Send exit code
con.send(bytes("16", "utf8"))

con.close()

