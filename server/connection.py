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

from threading import Thread

class Client(Thread):
	
	def __init__(self, con, addr):
		self.con = con
		self.addr = addr
	
	def run(self):
		i = 0
		while True:
			i = i + 1
			print (self.con.recv(4096).decode("ascii"))
			self.con.send(bytes("0", "ascii"))
			if (i == 2):
				self.con.close()
				break
