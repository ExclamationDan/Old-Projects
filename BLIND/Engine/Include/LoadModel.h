#pragma once
#include "Util.h"
#include "FileSystem.h"
#include "TinyXML\tinyxml2.h"

#include <GLEW\glew.h>
#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>

#include <iostream>
#include <string>
#include <sstream>

#include "Model.h"


using namespace tinyxml2;
using namespace std;


class CLoadModel
{
protected:
	XMLElement* SourceByID(XMLElement *XMLMesh,char* ID);

	XMLElement*	ParseMesh(XMLElement *Mesh,CModel *ModelD);
	void		ParseSource(XMLElement* XMLSource,CMesh* Mesh,CSource *Source);

public:

	CModel*	Load(string Path);



	CLoadModel(void);
	~CLoadModel(void);
};

