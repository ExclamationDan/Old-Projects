#pragma once

#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
using namespace std;



struct FPair
{
	string A;
	string B;

	FPair(string A1,string B1)
	{
		A = A1;
		B = B1;
	}
};


static vector<FPair> Paths;

// FileSystem is a simple path system that builds off of the .exe's residing directory.
// It must be setup with a directory in order to work properly.
// FSys.Setup(argv[0]); should be added near the top of main, as int main(int argc, char* argv[]) will supply the residing directory.
// You may supply any path you want for FSys.Setup(), though if you plan on FileSystem being useful, the dir should at least be valid.
// After that, you are free to use all facilities provided by the class.
// If you can't set up the filesystem, only utilitiy functions such as DirFix are useable because there is no directory dependency.

class CFileSystem
{
public:


	// Get the root, setup defaults [Read from config file?]
	void	Setup(char* Root);

	// General Aliases (Keywords to filepaths)
	// Root - Exe Dir
	// Data - General File structure (holds config, sound, ect folders)
	// Config,Models,Materials, and Sound point to the corresponding folders.

	string	AliasGet(string A); 
	string	AliasAdd(string A,string B);
	void	AliasCreate(string A,string B); // Make a new alias

	//Utility
	string	DirFix(string Dir);				// Fix the backslash characters.


	CFileSystem(void);
	~CFileSystem(void);
};


static CFileSystem	FSys; 