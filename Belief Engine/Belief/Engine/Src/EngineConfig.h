#pragma once
#include <stdio.h>
#include <string.h>

#include "FileSystem.h"
#include "Util.h"
#include "KeyGroup.h"

#include "ThirdParty\TinyXML\tinyxml2.h"


using namespace std;
using namespace tinyxml2;

class EngineConfig
{
public:
	typedef XMLAttribute XA;

	// This version of read is bad; if you plan on reading more than one var, read the entire file... unless its HUGE!
	CKeyLite	ReadSingle(char* File, char* Type,char* KeyWord, KEYTYPE T = KEY_STR)
	{
		XMLDocument doc;
		CKeyLite KG;
		
		if (doc.LoadFile(FSys.AliasAdd("Config",File).c_str()) == XML_SUCCESS)
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


	// This is not a deep read! (Future TODO?)
	// It does not check children of children, only children of Root.
	CKeyLite	ReadAll(char* File)
	{
		XMLDocument doc;
		CKeyLite KG;
		if (doc.LoadFile(FSys.AliasAdd("Config",File).c_str()) == XML_SUCCESS)
		{

			ParseAttrib(&KG,(XA*)doc.RootElement()->FirstAttribute());

			XMLElement *Node =  doc.RootElement()->FirstChildElement();

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
			Warning("Failed to load file |"+FSys.AliasAdd("Root",File)+"| for config parsing!",true);
			KG.Error("Failed to load file ["+(string)File+"] for config parsing!");
			return KG;
		}


	}

	void	ParseAttrib(CKeyLite* KG,XMLAttribute *Attr)
	{
		while(Attr != NULL)
			{
				KG->Add(Attr->Name(),const_cast<char*>( Attr->Value()));
				//cout << Attr->Name() << " " << Attr->Value() << endl;
				Attr = (XMLAttribute *) Attr->Next();
			}
	}


	EngineConfig(void)
	{

	}

	~EngineConfig(void)
	{

	}
};
