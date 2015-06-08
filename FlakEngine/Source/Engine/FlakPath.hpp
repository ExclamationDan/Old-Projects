#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <map>

#include "ThirdParty\TinyXML\tinyxml2.h"


#ifndef MSDOS
#include "Shlwapi.h"
#elif SYSV
#include  <fcntl.h>
#endif



using namespace std;

#ifndef MSDOS
bool cvtLPW2stdstring(std::string& s, const LPWSTR pw,UINT codepage = CP_ACP)
{
    bool res = false;
    char* p = 0;
    int bsz;
    bsz = WideCharToMultiByte(codepage,
        0,
        pw,-1,
        0,0,
        0,0);
    if (bsz > 0) {
        p = new char[bsz];
        int rc = WideCharToMultiByte(codepage,
            0,
            pw,-1,
            p,bsz,
            0,0);
        if (rc != 0) {
            p[bsz-1] = 0;
            s = p;
            res = true;
        }
    }
    delete [] p;
    return res;
}
#endif

static void FlakPrint(string Path)
{
	cout << "Path: " << Path << endl;
}


class FlakPath
{
public:
	FlakPath(void)  
	{
		Construct_DefaultPaths();
	};
	~FlakPath(void) {};

	map<string,string> Paths;
	// ***Directory Methods***
	string	Dir_Get_Residing()           
{

#ifndef MSDOS

TCHAR buffer[MAX_PATH];
GetModuleFileName(NULL,buffer,sizeof(buffer));
PathRemoveFileSpec(buffer);

string Path;
cvtLPW2stdstring(Path,buffer);



return  Dir_Fix(Path);

#elif SYSV
char buffer[260];
ssize_t len = ::readlink("/proc/self/exe", buffer, sizeof(buffer)-1);
if (len != -1) 
{
buffer[len] = '\0';
}
return  Dir_Fix(string(buffer));
#endif



}
	string  Dir_Get_Aliased(string Alias)
{
	return Paths[Alias];
}
	string  Dir_Fix(string Path) 
{
	int pos1,pos2,pos3;
	do
	{
		pos1 = Path.find('\\');
		if (pos1!=-1)  {Path.replace(pos1, 1, "/");}


		pos2 = Path.find("//");
		if (pos2!=-1)  {Path.replace(pos2, 2, "/");}

		pos3 = Path.find("///");
		if (pos3!=-1)  {Path.replace(pos3, 3, "/");}


	}
	while (pos1!=-1 || pos2!=-1 || pos3!=-1);

	return Path;

}
	string  Dir_Combine(string Root,string Sub) 
{
  	char Final[FILENAME_MAX]="";
	strcat_s(Final,Root.c_str());

	if (Sub[0] != '/')
	{strcat_s (Final,(char*)"/");strcat_s (Final,Sub.c_str());}
	else
	{strcat_s (Final,Sub.c_str());}
	return Dir_Fix(string(Final));

}
	string  Replace(string a, string b, string c)
{
	int pos ;
	do
	{
		pos = a.find(b);
		if (pos!=-1)  a.replace(pos, b.length(), c);
	}
	while (pos!=-1);
	return a;
}


	string	Dir_Add_Residing(char* Dir)
{
	return Dir_Combine(Dir_Get_Aliased("Root"),Dir);
}
	string  Dir_Add_Aliased(string Alias,string Path)
{
	return Dir_Combine(Dir_Get_Aliased(Alias),Path);
}


	// ***File Methods***
	bool	File_Exists(string Path)
{
	ifstream ifile(Path);
	if (ifile)
	{return true;}
	return false;
}
	string	File_Read(string Path) 
	{
		ifstream ifs(Path);
		if(!ifs.good()) 
		{
			cerr << "Couldn't find the file " << Path << endl;
			return "NULL - FAILED TO READ";
		}
		string str((istreambuf_iterator<char>(ifs)), istreambuf_iterator<char>());
		ifs.close();
		return str;
	}
	string	File_Read_Aliased(string Alias,string Path) 
	{ 
		return File_Read(Dir_Add_Aliased(Alias,Path));
	}
	string	File_Read_AliasedPure(string Alias) 
	{ 
		return File_Read(Dir_Get_Aliased(Alias));
	}

void Construct_DefaultPaths() 
{  
	Paths["Residing"     ] = Dir_Get_Residing();
	Paths["Root"         ] = Dir_Get_Aliased("Residing");
	Paths["Data"         ] = Dir_Add_Aliased("Residing","\\Data");
	Paths["Models"       ] = Dir_Add_Aliased("Data","\\Models");
	Paths["Shaders"      ] = Dir_Add_Aliased("Data","\\Shaders");
	Paths["Materials"	 ] = Dir_Add_Aliased("Data","\\Materials");
	Paths["Maps"		 ] = Dir_Add_Aliased("Data","\\Maps");
	Paths["Config"       ] = Dir_Add_Aliased("Data","\\Config");
	Paths["Configuration"] = Dir_Add_Aliased("Data","\\Config");
}
};


static FlakPath FPath;
