#pragma once

#include <GLEW\glew.h>
#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>
#include "TinyXML\tinyxml2.h"

#include <iostream>
#include <string>
#include <sstream>

#include "FileSystem.h"
#include "Util.h"
#include "Model.h"

using namespace tinyxml2;
using namespace std;

struct ModelPack
{
	CModel	*Model;
	string	Path;
	ModelPack(CModel *M,string P)
	{
		Model = M;
		Path = P;
	}
};

class CManagerModel
{
protected:
	// Remember to glDeleteBuffers(1, &V) - Add it later.

	XMLElement* SourceByID(XMLElement *XMLMesh,char* ID);
	XMLElement*	ParseMesh(XMLElement *Mesh,CModel *ModelD);
	void		ParseSource(XMLElement* XMLSource,CMesh* Mesh,CSource *Source);

public:
	vector<ModelPack>	mModelIndex;

	CModel*	Load(string Path);


	CManagerModel(void);
	~CManagerModel(void);
};

static CManagerModel ManagerModel;