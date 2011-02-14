# Class for file syncronization
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

import sqlite3
import os
from os.path import join, getsize, getmtime
import datetime

class Sync():
	
	def __init__(self, syncdir, con):
		# Normalize syncdir (end it with '/')
		if (not(syncdir.endswith('/'))):
			self._syncdir = syncdir + '/'
		else:
			self._syncdir = syncdir

		self._dbcon = sqlite3.connect('db')
		self._con = con

	def _checkForUpdatedFiles(self):
		pass	

	def sync(self):
		c = self._dbcon.cursor()
		for root, dirs, files in os.walk(self._syncdir):
			for name in files:
				path = join(root, name)[len(self._syncdir):]

				self._con.send(bytes("4 " + path, "utf8"))
				changetime = None
				if(self._con.recieve().decode("utf8") == "0"):
					# Send timestamp
					# TODO Check if everything is right with timezone etc.
					changetime = datetime.datetime.fromtimestamp(getmtime(join(root,name)))
					self._con.send(bytes("6 " + str(changetime), "utf8"))
				else:
					# Something went wrong
					self._con.send(bytes("16", "utf8"))
					exit()

				fileid = self._con.recieve().decode("utf8")
				c.execute("insert into filetable values(" + fileid + ", '" + path + "', '" + str(changetime) + "');")

		# Commit the query, after all files have been checked
		self._dbcon.commit()
		c.close()

