
#pragma once
#include <string>
#include <fstream>
#include <iostream>

#include "FileSystem.h"

#include <time.h>
#include <sstream>

using namespace std;


static void Log(string Text = "NULL", bool Write = false,bool Default = true)
{
	if (!Default)
		cout << Text << endl; 
	else
		cout << Text << endl; 

	if (Write)
	{
		CFileSystem FSys;
		ofstream file;
		file.open (FSys.AliasAdd("Root","DataLog.txt"), ios::app|std::ios::out);
		time_t raw;time (&raw);
		file << "\n" << asctime(localtime(&raw)) << ": " << Text << "\n";
		file.close();
	}
}

static void Warn(string Text = "NULL",bool Failure = false)
{
	if (!Failure)
		Log("\n <WARNING> " + Text,true,false);
	else
		Log("\n <FAILURE> " + Text,true,false);
}

static void Warning(string Text = "NULL",bool Failure = false)
{
	if (!Failure)
		Log("\n <WARNING> " + Text,true,false);
	else
		Log("\n <FAILURE> " + Text,true,false);
}

// Var to string stuff
static string ftos(float number)
{
ostringstream buffer;
buffer << number;
return buffer.str();
}

static string itos(int number)
{
	stringstream ss;
	ss << number;
	return ss.str();
}

// Safe String To Int/Float 
static int sstoi(string str)
{
	try
	{
		return stoi(str);
	}
	catch(...)
	{
		Warning("Failed to preform String to Int function on: "+str+" returning 0.",true);
		return 0;
	}
}

static float sstof(string str)
{
	try
	{
		return stof(str);
	}
	catch(...)
	{
		Warning("Failed to preform String to Float function on: "+str+" returning 0.",true);
		return 0;
	}
}

