#ifndef __INI_H__
#define __INI_H__

#include <string>
using namespace std;
class Ini {
	private:
		char * _path;
		string _trim(string toTrim);

	public:
		Ini(char * ipath);
		string getProperty(char * property);
};

#endif
