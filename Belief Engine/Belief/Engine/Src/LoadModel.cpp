#include "LoadModel.h"



CModel::CModel(void)
{
	OK = false;
}

CModel::~CModel(void)
{
}

void CModel::Draw()
{
	for (auto it : MeshData)
		it.Draw();
}

void CModel::AddMesh(CMesh XMLMesh)
{
	OK = true;
	MeshData.push_back(XMLMesh);
}


CLoadModel::CLoadModel(void)
{
}


CLoadModel::~CLoadModel(void)
{
}
	

CModel		CLoadModel::Load(string Path)
{
	CModel Ret_Model;
	
	Path = FSys.AliasAdd("Models",Path);
	XMLDocument doc;
	if (doc.LoadFile(Path.c_str()) ==  XML_SUCCESS)
	{
		XMLElement *Geo  = doc.RootElement()->FirstChildElement("library_geometries")->FirstChildElement("geometry");
		XMLElement *XMLMesh = Geo->FirstChildElement("mesh");

		while (Geo != NULL)
		{
			while (XMLMesh != NULL)
			{
				
				XMLMesh = ParseMesh(XMLMesh,&Ret_Model);
			}
			Geo = Geo->NextSiblingElement();
		}
		
		return Ret_Model;
	}
	else
	{
		Warning("Failed to load model: "+Path,true);
	}
	return Ret_Model;

}


XMLElement* CLoadModel::ParseMesh(XMLElement *XMLMesh,CModel* Model)
{
	// Parse a SINGLE Mesh
	// Parse XMLSources AND Triangles.

	CMesh Mesh;
	XMLElement *XMLSource = XMLMesh->FirstChildElement("source");
	XMLElement *Tri = XMLMesh->FirstChildElement("triangles");
	XMLElement *Input = Tri->FirstChildElement("input");
	Mesh.m_iTriangleCount = Tri->IntAttribute("count");



	while (Input != NULL)
	{
		CSource Source;

		if (strcmp(Input->Attribute("semantic"),"VERTEX") == 0) 
		{
			Source.mID = XMLMesh->FirstChildElement("vertices")->FirstChildElement("input")->Attribute("source");
		}
		else 
		{
			Source.mID		=	Input->Attribute("source");
		}

		Source.mType	=	(char*) Input->Attribute("semantic");
		Source.mOffset	=	Input->IntAttribute("offset");
		Source.mID		=	Source.mID.erase(0, 1); // Remove the pound symbol.

		ParseSource(SourceByID(XMLMesh,(char*)Source.mID.c_str()),&Mesh,&Source);
		Input = Input->NextSiblingElement("input");
	}

	// [Get index list]

	// [Matrix setup]

	// Let's hope we've added everything needed in these loops.
	Model->AddMesh(Mesh);

	return XMLMesh->NextSiblingElement("mesh");

}


void		CLoadModel::ParseSource(XMLElement* XMLSource,CMesh* Mesh,CSource *Source)
{
	// Parse a SINGLE Source.
	XMLElement *_array = XMLSource->FirstChildElement("float_array");
	Source->mCount = _array->IntAttribute("count");
	
	string token,line,text;
	text = (char*)(_array->GetText());
	istringstream iss(text);

	int i = -1;
	while(getline(iss, token, ' '))
	{
		istringstream iss2(token);
		while(getline(iss2,line,'\n'))
		{
			if (i >= 0) {Source->mData.push_back(atof(line.c_str()));}
			i++;
		}
	}


	Source->mStride = _array->NextSiblingElement("technique_common")->FirstChildElement("accessor")->IntAttribute("stride");
	Mesh->Update_WithSource(Source); // This is ok, we extract source data, not save a copy of the source.

}


XMLElement* CLoadModel::SourceByID(XMLElement *XMLMesh,char* ID)
{
	XMLElement *XMLSource = XMLMesh->FirstChildElement("source");
	while (XMLSource != NULL)
	{
		if (strcmp(XMLSource->Attribute("id"),ID) == 0)
		{
			return XMLSource;
		}
		XMLSource = XMLSource->NextSiblingElement("source");
	}
	Warning("SourceByID: Failed to find ID: "+(string)ID,true);
	return NULL;
}