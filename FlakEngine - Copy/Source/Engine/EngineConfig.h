#pragma once
#include <stdio.h>
#include <string.h>

#include "FlakFuncs.hpp"
#include "FlakPath.hpp"

#include "ThirdParty\TinyXML\tinyxml2.h"
#include "KeyGroup.h"

using namespace std;
using namespace tinyxml2;

class EngineConfig
{
public:

	typedef tinyxml2::XMLAttribute XA;
	CKeyLite	ReadSingle(char* File, char* Type,char* KeyWord, KEYTYPE T = KEY_STR)
	{
		tinyxml2::XMLDocument doc;
		CKeyLite KG;
		if (doc.LoadFile(FPath.Dir_Add_Aliased("Config",File).c_str()) == XML_SUCCESS)
		{

			switch (T)
			{
			case KEY_STR:
				KG.Add(Type,(char*) doc.RootElement()->FirstChildElement(Type)->Attribute(KeyWord));
				break;

			case KEY_INT:
				KG.Add(Type,sstoi(doc.RootElement()->FirstChildElement(Type)->Attribute(KeyWord)));
				break;

			case KEY_FLOAT:
				KG.Add(Type,sstof(doc.RootElement()->FirstChildElement(Type)->Attribute(KeyWord)));
				break;
			}
			return KG;

		}


		else
		{
			cout << "Failed to load XML file.\n";		
			KG.Error("Failed to load file ["+(string)File+"] for config parsing!");
			return KG;
		}

	}

	CKeyLite	ReadAll(char* File)
	{
		tinyxml2::XMLDocument doc;
		CKeyLite KG;
		if (doc.LoadFile(FPath.Dir_Add_Aliased("Config",File).c_str()) == XML_SUCCESS)
		{

			ParseAttrib(&KG,(XA*)doc.RootElement()->FirstAttribute());

			tinyxml2::XMLElement *Node =  doc.RootElement()->FirstChildElement();

			// This is not a deep read! 
			// It does not check children of children, only children of Root.
			while(Node != NULL)
			{
				ParseAttrib(&KG,(XA*) Node->FirstAttribute());
				if (Node->NoChildren())
				{
					Node = Node->NextSiblingElement();
					continue;
				}
				else
				{
					//ParseChildren(&KG,Node->FirstChildElement()); - TODO
					Node = Node->NextSiblingElement();

				}
				
			}
			return KG;
		}
		else
		{
			Warning("Failed to load file ["+(string)File+"] for config parsing!",true);
			KG.Error("Failed to load file ["+(string)File+"] for config parsing!");
			return KG;
		}


	}

	void	ParseAttrib(CKeyLite* KG,tinyxml2::XMLAttribute *Attr)
	{
		while(Attr != NULL)
			{
				KG->Add(Attr->Name(),const_cast<char*>( Attr->Value()));
				//cout << Attr->Name() << " " << Attr->Value() << endl;
				Attr = (tinyxml2::XMLAttribute *) Attr->Next();
			}
	}


	EngineConfig(void)
	{

	}

	~EngineConfig(void)
	{

	}
};