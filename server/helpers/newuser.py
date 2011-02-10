#!/usr/bin/env python

# Insert a new user into the database
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

def getProperty(configFile, section, prop):
	try:
		import configparser
		config = configparser.ConfigParser()

		config.read(configFile)

		return config[section][prop]

	except KeyError:
		print ('Configuration file does not exist, or is corrupted. Please create it using helpers/makeconfig.py');
		return ''

# Postgresql connection made using py-postgresql - http://python.projects.postgresql.org/
import postgresql
# Create configuration file first

username = getProperty('../config.ini', 'db', 'username')
password = getProperty('../config.ini', 'db', 'password')
host = getProperty('../config.ini', 'db', 'host')
port = getProperty('../config.ini', 'db', 'port')
database = getProperty('../config.ini', 'db', 'database')

db = postgresql.open(user = username, password = password, host = host, port = port, database = database)

newemail = input("Email: ")
import getpass
newpassword = getpass.getpass("Password: ")

stmt = db.prepare('INSERT INTO usertable (email, password) VALUES ($1, $2)')

import hashlib
ex = stmt(newemail, hashlib.sha1(newpassword.encode("ascii")).hexdigest())
