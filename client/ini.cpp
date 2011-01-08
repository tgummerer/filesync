#include <iostream>
#include <fstream>
#include <string>
#include "ini.h"

using namespace std;
Ini::Ini(char * ipath) {
	path = ipath;
}

// get the folder which should be synchronized
string Ini::getSyncPath() {
	ifstream stream;
	string buffer;	
	stream.open(path);
	
	if(!stream.is_open()) {
		// Problem with opening the input stream
		cerr << "Error, ini file could not be opened.\n";
		return "";
	}

	while(!stream.eof()) {
		getline (stream, buffer);
		if (buffer.substr(0, 8) == "syncpath") {
			stream.close();
			// TODO: Don't make it rely on wellformed config file.
			return buffer.substr(11);
		}
	}

	stream.close();
	// The syncpath variable has not been found in the ini file
	cerr << "Error, syncpath is not defined in the config ini file.\n";
	return "";
}
