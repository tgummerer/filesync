# Easy db access
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

import postgresql

class Db():
	
	_db = None
	
	def _getProperty(self, configFile, section, prop):
		try:
			import configparser
			config = configparser.ConfigParser()

			config.read(configFile)

			return config[section][prop]

		except KeyError:
			print ('Configuration file does not exist, or is corrupted. Please create it using helpers/makeconfig.py');
			return ''


	def __init__(self):
		username = self._getProperty('config.ini', 'db', 'username')
		password = self._getProperty('config.ini', 'db', 'password')
		host = self._getProperty('config.ini', 'db', 'host')
		port = self._getProperty('config.ini', 'db', 'port')
		database = self._getProperty('config.ini', 'db', 'database')

		self._db = postgresql.open(user = username, password = password, host = host, port = port, database = database)

	def executeQuery(self, query):
		self._db.execute(query)

	def executeSelect(self, query):
		return self._db.prepare(query)
