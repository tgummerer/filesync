# Connection thread
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

import threading
import socket
import db

class Client(threading.Thread):
	
	def __init__(self, con, addr):
		threading.Thread.__init__(self)
		self.con = con
		self.addr = addr

		# Set up db connection
		self._db = db.Db()

	def _checkUsernamePassword(self, username, password):
		result = self._db.executeSelect("select * from usertable where email = '" + username + "' and password = '" + password + "'")
		if (result.first() is None):
			return False
		else:
			# Return userid
			return result.first()[0]

	def _checkUsername(self, username):
		# For now always accept the username. Might change in future versions
		self.con.send(bytes("0", "ascii"))

	def _checkPassword(self, password):
		self._userid = self._checkUsernamePassword(self._username, password)
		if ((self._username != None) and (password != None) and 
			(self._userid != None)):
			self.con.send(bytes("0", "ascii"))
		else:
			self.con.send(bytes("1", "ascii"))
			thread.exit()

	def _newFile(self, filename):
		self._db.executeQuery("insert into filetable (userid, filename) values ("+self._userid+", '"+filename+"')")
		
	def run(self):
		# Define this variables here, to have them available in the whole method
		username = None
		password = None
		while True:
			try:
				rec = self.con.recv(4096).decode("ascii")
				# Split the string on the first occurence of a blank. Protocol says all send strings are
				# a number followed by a blank, followed by the thing that is sent
				split = rec.partition(' ')

				if (split[0] == '0'):			# Username
					self._username = split[2]
					self._checkUsername(self._username)

				elif (split[0] == '1'):  		# Password
					self._password = split[2]
					self._checkPassword(self._password)
					
				elif (split[0] == '2'):			# New file
					filename = split[2]
					self._newfile(filename)

				elif (split[0] == '3'):			# Changed file
					fileid = split[2]
					self._db.executeQuery("update filetable set lastchange = now() where fileid = " + fileid)

				elif (split[0] == '16'):		# Exit
					break

			except socket.error:
				break

		#_db.close()
