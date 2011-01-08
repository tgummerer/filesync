#ifndef __INI_H__
#define __INI_H__
#include <string>
using namespace std;
class Ini {
	private:
		char * path;

	public:
		Ini(char * ipath);
		string getSyncPath();
};

#endif
