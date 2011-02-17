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
from os.path import join, getsize, getmtime, getatime
import datetime
import time
import random

class Sync():
	
	def __init__(self, syncdir, con):
		# Normalize syncdir (end it with '/')
		if (not(syncdir.endswith('/'))):
			self._syncdir = syncdir + '/'
		else:
			self._syncdir = syncdir

		self._dbcon = sqlite3.connect('db')
		self._con = con

	def _sendFile(self, path):
		sendfile = open(path, 'rb')
		data = sendfile.read()

		self._con.sendall(bytes("7 " + str(len(data)), "utf8")) # Send the length as a fixed size message
		self._con.recieve(1)

		self._con.sendall(data)

		# Get Acknowledgement
		self._con.recieve(1) # Just 1 byte

	def sync(self):
		c = self._dbcon.cursor()
		# TODO Check if some file hase changed. Check by checking st_atime for syncpath
		c.execute ("select max(lastchange) from filetable")
		# Initialize to a very old time, for the first time the syncronization runs
		stime = "1970-01-01 00:00:00"
		for row in c:
			if (not(row[0] == None)):
				stime = row[0]

		# Only do something if a file has changed
		time_format = "%Y-%m-%d %H:%M:%S"
		if (time.mktime(time.strptime(stime, time_format)) < getatime(self._syncdir)):
			c.execute ("select * from filetable")
			i = None
			rows = {}
			for row in c:
				rows[row[1]] = row

			for root, dirs, files in os.walk(self._syncdir):
				for name in files:
					path = join(root, name)[len(self._syncdir):]

					
					if (path in rows):		# File exists, update or leave it alone
						if (time.mktime(time.strptime(rows[path][2], time_format)) < getmtime(join(root, name))):
											# File has to be updated
							self._con.send(bytes("5 " + str(rows[path][0]), "utf8"))
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

							if (self._con.recieve().decode("utf8") == "0"):
								self._sendFile(join(root, name))

							# Just wait for the message, nothing else
							self._con.recieve()
							c.execute("update filetable set lastchange = '" + str(changetime) + "' where fileid = " + str(rows[path][0]))

						else:				# Leave file alone
							pass
					else:					# File does not exist, send it to the server

						self._con.send(bytes("4 " + path, "utf8"))
						changetime = None
						if(self._con.recieve().decode("utf8") == "0"):
							# Send timestamp
							# TODO Check if everything is right with timezone etc.
							changetime = datetime.datetime.fromtimestamp(getmtime(join(root,name)))
							self._con.send(bytes("6 " + str(changetime), "utf8"))
						else:
							print ("Error sending new file")
							# Something went wrong
							self._con.send(bytes("16", "utf8"))
							exit()

						print("start sending file")
						# Send file
						ack = self._con.recieve().decode("utf8")
						#print ("Ack " + ack)
						if (ack == "0"):
							print ("ack")
							print(join(root, name))
							self._sendFile(join(root, name))


						print("enter file in database with fileid: ")
						fileid = self._con.recieve().decode("utf8")
						print (fileid)
						c.execute("insert into filetable values (" + fileid + ", '" + path + "', '" + str(changetime) + "');")
						self._dbcon.commit()
						print ("send next file")

			# Commit the query, after all files have been checked
			self._dbcon.commit()
			c.close()

