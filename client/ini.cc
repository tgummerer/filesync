#include <iostream>
#include <fstream>
#include <string>
#include "ini.h"

using namespace std;
Ini::Ini(char * ipath) {
	_path = ipath;
}

string Ini::_trim(string toTrim) {
	int start = toTrim.find_first_not_of(" \t");
	int end = toTrim.find_last_not_of(" \t");

	return toTrim.substr(start, end - start + 1);
}

string Ini::getProperty(char * property) {
	ifstream stream;
	string prop = property;
	string buffer;
	stream.open(_path);

	if (!stream.is_open()) {
		cerr << "Error opening ini file.\n";
		return "";
	}

	while(!stream.eof()) {
		getline(stream, buffer);
		if (buffer.substr(0, prop.length()) == prop) {
			// We found what we wanted, no need to keep the stream open longer
			stream.close();
			// The position of the equal sign
			int equalposition;
			equalposition = buffer.find_first_of("=");
			string syncpath = buffer.substr(equalposition+1);

			// Remove initial and trailing spaces from the string
			syncpath = Ini::_trim(syncpath);
			return syncpath;
		}
	}

	// Nothing found, close the stream anyway
	stream.close();

	cerr << "Error finding " << prop << " in the ini file\n";
	return "";
}
