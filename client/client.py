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

import hashlib
import getpass

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

def getUserData():
	import configparser
	config = configparser.ConfigParser()
	config.read(configFile)
	config['userdata'] = {}
	config['userdata']['username'] = input("Username: ")
	# Know this should not be done, but I don't like to write more than one line for it
	config['userdata']['password'] = hashlib.sha1(getpass.getpass("Password: ").encode("utf8")).hexdigest()

	with open('config.ini', 'w') as configfile:
		config.write(configfile)

def getSyncData(con):
	import configparser
	config = configparser.ConfigParser()
	config.read(configFile)
	config['syncdata'] = {}
	con.send(bytes("2", "utf8"))
	config['syncdata']['clientid'] = con.recieve().decode("utf8")

	with open('config.ini', 'w') as configfile:
		config.write(configfile)

###############################################################################

# Path to configuration file
configFile = 'config.ini'

# Method to get the syncronization path
# getSyncPath(configFile)
import connection
con = connection.Connection(getProperty(configFile, 'config', 'serveraddress'))

# Credentials not in the config file, ask the user for them and write them to config file
if (not(isInConfig(configFile, 'userdata'))):
	getUserData()

	
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

if (not(isInConfig(configFile, 'syncdata'))):
	getSyncData(con)

clientid = getProperty(configFile, 'syncdata', 'clientid')
con.send(bytes("3 " + clientid, "utf8"))

import sync
import time
syncdir = getProperty(configFile, 'config', 'syncpath')
sy = sync.Sync(syncdir, con)
i = 0
while True:

	if (i == 11):
		# Force checking if there is something to sync every minute. Sometimes the check for the time is not enough.
		i = 0
		sy.sync(True)
	else:
		sy.sync()
	time.sleep(5) # Wait 5 seconds until the next try of syncing
	i += 1

# Send exit code
con.send(bytes("16", "utf8"))

con.close()

