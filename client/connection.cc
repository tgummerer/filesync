/* Build a connection to the server
   Copyright (C) 2011 Thomas Gummerer

This file is part of Filesync.

Filesync is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Filesync is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Filesync.  If not, see <http://www.gnu.org/licenses/>.  */

#include <iostream>

#include <sys/socket>
#include <sys/types>
#include <netinet/in>
#include "connection.h"

using namespace std;
Connection::Connection(string serverAddress) {
	struct hostent *host;
	struct sockaddr_in server_addr;

	host = gethostbyname(serverAddress);
	
	if ((sock = socket (AF_INET, SOCK_STREAM, 0)) == -1) {
		cerr << "Socket failed";
		exit(1);
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(13013);
	server_addr.sin_addr = *((struct in_addr *)host->h_addr);
	bzero(&(server_addr.sin_zero), 8);

	if (connect(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1) {
		cerr << "Error connecting";
		exit(1);
	}
}

void send (string message) {
	;
}

void disconnect() {
	;
}
