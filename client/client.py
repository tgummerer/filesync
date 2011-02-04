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

def getSyncPath(configFile):
	try:
		import configparser
		config = configparser.ConfigParser()

		config.read(configFile)

		return config['config']['syncpath']

	except KeyError:
		print ('Configuration file does not exist. Please create it using helpers/makeconfig.py');
		return '';

print (getSyncPath('config.ini'))

