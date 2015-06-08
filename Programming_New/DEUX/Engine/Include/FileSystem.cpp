#include "FileSystem.h"
#include "Util.h"


		CFileSystem::CFileSystem(void)
{
}

		CFileSystem::~CFileSystem(void)
{
}

void	CFileSystem::Setup(char* Root)
{
		std::string directory = Root;
		size_t find = directory.find_last_of("/\\");
		AliasCreate("Root",directory.substr(0,find));
		AliasCreate("Data",AliasAdd("Root","Data"));
		AliasCreate("Config",AliasAdd("Data","Config"));
		AliasCreate("Models",AliasAdd("Data","Models"));
		AliasCreate("Materials",AliasAdd("Data","Materials"));
		AliasCreate("Sound",AliasAdd("Data","Sound"));
}

void	CFileSystem::AliasCreate(string A, string B)
{
	Paths.push_back(FPair (A,B));
}

string	CFileSystem::AliasGet(string A)
{

	// No longer supporting C++ 11 standards
	// Before: for(vector<FPair>::iterator it = Paths.begin();it != Paths.end();it++)


	for(auto it = Paths.begin(); it != Paths.end(); it++) 
	{
		if(it->A == A)
			return it->B;
	}
	return itos(Paths.size());
}

string	CFileSystem::AliasAdd(string A, string B)
{
	return DirFix(AliasGet(A)+"/"+B);
}

string  CFileSystem::DirFix(string Path) 
{
	// Sometimes when merging paths, back/forward slashes will be duplicated or mixed; this function formats them.

	string Token1 = "\\"; // Escape Char 
	string Token2 = "//"; // Normal
	int Pos1, Pos2;

		do
		{
			Pos1 = Path.find(Token1);
			if (Pos1!=-1)  {Path.replace(Pos1, Token1.length(), "/");}

			Pos2 = Path.find(Token2);
			if (Pos2!=-1)  {Path.replace(Pos2, Token2.length(), "/");}
		}
		while( (Pos1 != string::npos) || (Pos2 != string::npos) );


	return Path;

}