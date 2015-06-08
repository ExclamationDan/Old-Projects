#include "ManagerModel.h"

CManagerModel::CManagerModel(void)
{
}


CManagerModel::~CManagerModel(void)
{
}


CModel*		CManagerModel::Load(string Path)
{
	for (auto it = mModelIndex.begin();it != mModelIndex.end(); it++) 
	{
		if (FSys.AliasAdd("Models",Path) == it->Path)
		{
			cout << "ManagerModel: Returning Allocated Buffer.\n";
			return it->Model;
		}
	}

	cout << "ManagerModel: Allocating New Buffer\n";


	CModel *Ret_Model = new CModel;
	
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
				
				XMLMesh = ParseMesh(XMLMesh,Ret_Model);
			}
			Geo = Geo->NextSiblingElement();
		}
		cout << "Returned Valid Model.\n";

		Ret_Model->Finalize();
		mModelIndex.push_back(ModelPack(Ret_Model,Path));
		return Ret_Model;
	}
	else
	{
		Warning("Failed to load model: "+Path,true);
	}
	return NULL;

}


XMLElement* CManagerModel::ParseMesh(XMLElement *XMLMesh,CModel* Model)
{
	// Parse a SINGLE Mesh
	// Parse XMLSources AND Triangles.

	CMesh Mesh;
	XMLElement *XMLSource = XMLMesh->FirstChildElement("source");
	XMLElement *Tri = XMLMesh->FirstChildElement("triangles");
	XMLElement *Input = Tri->FirstChildElement("input");
	//Mesh.mTriangleCount = Tri->IntAttribute("count");



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


		// This is actually <p>, aka an index list.
		Mesh.mIndex  = gusVector_SplitString((char*)Tri->FirstChildElement("p")->GetText(),' ');


		ParseSource(SourceByID(XMLMesh,(char*)Source.mID.c_str()),&Mesh,&Source);
		Input = Input->NextSiblingElement("input");
	}




	// [Matrix setup]

	// Let's hope we've added everything needed in these loops.
	Model->AddMesh(Mesh);

	return XMLMesh->NextSiblingElement("mesh");

}


void		CManagerModel::ParseSource(XMLElement* XMLSource,CMesh* Mesh,CSource *Source)
{
	// Parse a SINGLE Source.
	XMLElement *_array = XMLSource->FirstChildElement("float_array");
	Source->mCount = _array->IntAttribute("count");


	Source->mData = fVector_SplitString((char*)(_array->GetText()), ' '); // Grab all dem good floats, mhhh yeah. We all know it good.


	Source->mStride = _array->NextSiblingElement("technique_common")->FirstChildElement("accessor")->IntAttribute("stride");
	Mesh->Extract_Source(Source); // This is ok, we extract source data, not save a copy of the source. (Silly end of block memory deletion)

}


XMLElement* CManagerModel::SourceByID(XMLElement *XMLMesh,char* ID)
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