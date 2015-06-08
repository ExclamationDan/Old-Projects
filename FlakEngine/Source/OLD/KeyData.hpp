#pragma once
#include "FlakFuncs.hpp"
#include "Model.hpp"
#include <map>


// Keydata is a class made for ENTITY that holds custom and common data, such as health, and other presets.
using namespace std;

class CKeyData
{
private:

public:

	map<string,string> KeyData;
	map<string,string>::iterator it;

	// Adding / Deleting
	void	Addf(string Key,float Value)
	{
		if (!Exists(Key))
		{
			KeyData[Key] =  ftos(Value);
		}
		else
		{
			FLog("KeyData: "+Key+" already exists! Data ignored.",true);
		}
	}

	void	Addi(string Key,int Value)
	{
		if (!Exists(Key))
		{
			KeyData[Key] =  itos(Value);
		}
		else
		{
			FLog("KeyData: "+Key+" already exists! Data ignored.",true);
		}
	}

	void	Add(string	Key,string Value)
	{
		if (!Exists(Key))
		{
			KeyData[Key] = Value;
		}
		else
		{
			FLog("KeyData: "+Key+" already exists! Data ignored.",true);
		}
	}

	void	Delete(string Key)
	{
		if (Exists(Key))
		{
			KeyData.erase(KeyData.find(Key));
		}
		else
		{
			FLog("KeyData: "+Key+" does not exist, failed to delete.",true);
		}
	}


	// Utility
	bool	Exists(string Key)
	{
		it = KeyData.find(Key); 
		if ( it != KeyData.end() )
			{return true;}
		else
		{
			FLog("KeyData: "+Key+" does not exist, exist check failed",true);
			return false;
		}
	}

	void	Set(string Key,string Value)
	{
			if (!Exists(Key))
			{
				Add(Key,Value);
			}
			else
			{
				KeyData[Key] = Value;
			}

	}

	void	Seti(string Key,int Value)
	{
			if (!Exists(Key))
			{
				Addi(Key,Value);
			}
			else
			{
				KeyData[Key] = itos(Value);
			}
	}

	void	Setf(string Key,float Value)
	{
			if (!Exists(Key))
			{
				Addf(Key,Value);
			}
			else
			{
				KeyData[Key] = ftos(Value);
			}

	}

	// Getting
	string	Get(string Key)
	{
		if(Exists(Key))
		{
			return KeyData[Key];
		}
		else
	}

	int		Geti(string Key)
	{
		if(Exists(Key))
		{
			return stoi(KeyData[Key]);
		}
	}

	char*	Getc(string Key)
	{
		if(Exists(Key))
		{
			return (char*) KeyData[Key].c_str();
		}
	}


	CKeyData() {}
	~CKeyData() 
	{

	}
};

