#include <string>
#include <iostream>
#include "ini.h"

using namespace std;

int main ()
{
	char * pathToIni = "./config.ini";
	string syncpath;
	Ini::Ini * inifile = new Ini::Ini(pathToIni);
	syncpath = inifile->getProperty("syncpath");
	cout << syncpath << "\n";
}
