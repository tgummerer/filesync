#!/usr/bin/env python

# Simple echo server for testing
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

import socket

s = socket.socket()
host = socket.gethostname()
port = 13131
s.bind((host, port))

s.listen(5)
while True:
   con, addr = s.accept()
   print ('Got connection from', addr)
   echo = con.recv(4096)
   con.send(echo)
   con.close()

