# Reading ini files
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
 
CC = g++

BIN = filesync 
OBJS = client.o ini.o
CFLAGS = 

$(BIN): $(OBJS)
	$(CC) -o $(BIN) $(OBJS)

client.o: client.cc

ini.o: ini.cc ini.h

clean:
	rm $(BIN) $(OBJS)
