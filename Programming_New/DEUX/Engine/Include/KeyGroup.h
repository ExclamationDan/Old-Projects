#pragma once

#include "FlakFuncs.hpp"
#include "FlakPath.hpp"
#include "vector"
using namespace std;

enum KEYTYPE  {KEY_STR = 1,KEY_INT,KEY_FLOAT};

// Should we discontinue int and float support, and just convert the string to int or float?
// Opted to keep the two; if it is a string and another type is asked, it is converted via sstoi/sstof.

struct Key
{
	// Key Name
	string		m_sKey;

	// char* in union was getting its pointed var deleted when the assignment block ended
	// Changed to string and was forced to remove it from union.
	string		m_sValue;

	union
	{
	int			m_iValue;
	float		m_fValue;
	
	};
	KEYTYPE	Type;
};

struct Root
{
	string m_sRoot;
	vector<Key>	Keys;

	bool Key_Set(string K,char *V)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)
			{
				it->m_sValue = V;
				it->Type = KEY_STR;
				return true;
			}		
		}
		return false;
	}
	bool Key_Set(string K,int V)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)
			{
				it->m_iValue = V;
				it->Type = KEY_INT;
				return true;
			}		
		}
		return false;
	}
	bool Key_Set(string K,float V)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)
			{
				it->m_fValue = V;
				it->Type = KEY_FLOAT;
				return true;
			}		
		}
		return false;
	}

	// We don't allow keys with the same name, if it exists, it gets set to V.

	void Key_Add(Key K)
	{
	if (!Key_Exists(K.m_sKey))
		{
			Keys.push_back(K);
		}
	}
	void Key_Add(string K,char *V)
	{
		if (!Key_Set(K,V))
		{
			Key TK;
			TK.m_sKey = K;
			TK.m_sValue =  V;
			TK.Type = KEY_STR;
			Keys.push_back(TK);
		}
	}
	void Key_Add(string K,int V)
	{
		if (!Key_Set(K,V))
		{
			Key TK;
			TK.m_sKey = K;
			TK.m_iValue = V;
			TK.Type = KEY_INT;
			Keys.push_back(TK);
		}
	}
	void Key_Add(string K,float V)
	{
		if (!Key_Set(K,V))
		{
			Key TK;
			TK.m_sKey = K;
			TK.m_fValue = V;
			TK.Type = KEY_FLOAT;
			Keys.push_back(TK);
		}
	}

	// Getstr will convert int/float to string.
	char*	Key_Getstr(string K)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)	
				{

				if (it->Type == KEY_INT)
					{
						return (char*) itos(it->m_iValue).c_str();
					}
				else if (it->Type == KEY_FLOAT)
					{
						return (char*) ftos(it->m_iValue).c_str();
					}

				return (char*)it->m_sValue.c_str();		
				}
		}
		return "NULL";
	}
	// Geti/Getf will convert string to int/float.
	int		Key_Geti(string K)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)	
				{
					if (it->Type == KEY_STR)
						{
							return sstoi(it->m_sValue);
						}
					return it->m_iValue;
				}
		}
		return 0;
	}
	float	Key_Getf(string K)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)	
				{
					if (it->Type == KEY_STR)
						{
							return sstoi(it->m_sValue);
						}
					return it->m_fValue;
				}	
		}
		return 0.0f;
	}


	void Root_PrintAll()
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			switch(it->Type)
			{
			case KEY_STR:
				cout << "String\n";
				cout << "Key: " << it->m_sKey << " Value: " << it->m_sValue << "\n";
				break;

			case KEY_INT:
				cout << "Int\n";
				cout << "Key: " << it->m_sKey << " Value: " << it->m_iValue << "\n";
				break;

			case KEY_FLOAT:
				cout << "Float\n";
				cout << "Key: " << it->m_sKey << " Value: " << it->m_fValue << "\n";
				break;

			default:
				cout <<"Key " << it->m_sKey << " Value: " << "NO TYPE FOUND, CANNOT PRINT!\n";
				break;

			}
		}
	}

	void Key_Delete(string K)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)
			{
				Keys.erase(it);
				break;
			}		
		}
	}
	bool Key_Exists(string K)
	{
		vector<Key>::iterator it;
		for (it = Keys.begin(); it != Keys.end();it++)
		{
			if (it->m_sKey == K)
				return true;	
		}
		return false;
	}
};


// (SINGLE ROOT)
// (K)   (V)
// ect...
class CKeyLite
{
public:
	Root	Data;
	friend CKeyLite operator+(CKeyLite K1, CKeyLite K2);

	bool	Exists(string K)
	{
		return Data.Key_Exists(K);
	}
	void	Delete(string K)
	{
		Data.Key_Delete(K);
	}
	void	PrintAll()
	{
		Data.Root_PrintAll();
	}

	bool	Set(string K,char *V)
	{
		return Data.Key_Set(K,V);
	}
	bool	Set(string K,int V)
	{
		return Data.Key_Set(K,V);
	}
	bool	Set(string K,float V)
	{
		return Data.Key_Set(K,V);
	}

	void	Add(Key K)
	{
		Data.Key_Add(K);
	}
	void	Add(string K, char *V)
	{
		Data.Key_Add(K,V);
	}
	void	Add(string K, int V)
	{
		Data.Key_Add(K,V);
	}
	void	Add(string K, float V)
	{
		Data.Key_Add(K,V);
	}

	int		Geti(string K)
	{
		return Data.Key_Geti(K);
	}
	float	Getf(string K)
	{
		return Data.Key_Getf(K);
	}
	char*	Getstr(string K)
	{
		return Data.Key_Getstr(K);
	}

	void	Error(string Fail = "Population Failure")
	{
		Add("CKEYLITE_LAST_ERROR",(char*) Fail.c_str() );
	}


	CKeyLite() { Data.m_sRoot = "KEYLITE:DATA_ROOT";}
	CKeyLite(string RootName) { Data.m_sRoot = RootName;}


	~CKeyLite() { }
};

	// Overwriting isn't supported. K1 will keep its keys.
	CKeyLite operator+(CKeyLite K1, CKeyLite K2)
	{
		vector<Key>::iterator it;
		for (it = K2.Data.Keys.begin();it != K2.Data.Keys.end();it++)
			{
				K1.Add(*it);
			}
		return K1;
	}
