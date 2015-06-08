#pragma once

#include "Model.hpp"
#include "FlakFuncs.hpp"

#include "Mesh.hpp"
#include <stdio.h>
#include <iostream>
#include <sstream>

#include "ThirdParty\TinyXML\tinystr.h"
#include "ThirdParty\TinyXML\tinyxml.h"

using namespace std;

class Collada
{

public:

	Collada()  {}
	~Collada() {}


  CModel* Read(char* Path)
{
	TiXmlDocument File(Path);
	if (File.LoadFile())
	{
		FLog("Load OK.");

		TiXmlElement *mesh, *source, *triangles, *input, *temp,*_array, *accessor,*ColSource,*p, *Node, *inst,*img;


		TiXmlElement* Geometry = File.RootElement()->FirstChildElement("library_geometries")->FirstChildElement("geometry");


		CModel *Model = new CModel;

		while(Geometry != NULL)
		{
			mesh	  =		Geometry->FirstChildElement("mesh");
			triangles =		mesh->FirstChildElement("triangles");
			input	  =		triangles->FirstChildElement("input");

			while(mesh != NULL) 
			{         
				CMesh* MeshData = new CMesh;

				while (input != NULL)
				{

					CSource *Source = new CSource;
					Source->mType = (char*) input->Attribute("semantic");
					Source->mOffset = atoi(input->Attribute("offset")); 


					if (!strcmp(Source->mType,"VERTEX"))
					{Source->mID = std::string(mesh->FirstChildElement("vertices")->FirstChildElement("input")->Attribute("source"));}
					else
					{Source->mID = std::string(input->Attribute("source"));}

					Source->mID = Source->mID.erase(0, 1);


					temp = mesh->FirstChildElement("source");
					while(temp != NULL)
					{
						if ( !(Source->mID.compare(temp->Attribute("id"))) )
						{break;}
						temp = temp->NextSiblingElement("source");
					}

					_array = temp->FirstChildElement("float_array");
					Source->mCount = atoi(_array->Attribute("count"));



					char *text = (char*)(_array->GetText());
					Source->mData = new float[Source->mCount];
					Source->mData[0] = atof(strtok(text, " ")); 


					for(int index = 1; index < Source->mCount; index++) 
					{(Source->mData)[index] = atof(strtok(NULL, " "));}

					accessor = _array->NextSibling("technique_common")->FirstChildElement("accessor");
					Source->mStride = stoi(accessor->Attribute("stride"));


					MeshData->Update_WithSource(Source);

					delete Source;
					input = input->NextSiblingElement("input");
				}
				p = triangles->FirstChildElement("p");

				string text = ((string) p->GetText());
					
		
				// This makes models without Three elements per vertex invalid!!!!
				// Any three of  Vertex, Normal, Texcoord, or color will work, no less, or more!

				
				MeshData->mIndex.mCount = (stoi(triangles->Attribute("count"))*9);


				if (triangles->Attribute("material"))
				{ 
					if (File.RootElement()->FirstChildElement("library_images") != NULL)
						MeshData->mTexture = FPath.Dir_Fix(string((char*)File.RootElement()->FirstChildElement("library_images")->FirstChildElement("image")->FirstChildElement("init_from")->GetText()));
					else
						MeshData->mTexture = "NULL";
				}
				else 
				{MeshData->mTexture = "NULL";}


				MeshData->mIndex.mData = new int[MeshData->mIndex.mCount];

				(MeshData->mIndex.mData)[0] = atoi(strtok((char*)text.c_str(), " ")); 
				for(int index=1; index<MeshData->mIndex.mCount; index++) 
				{
					(MeshData->mIndex.mData)[index] = atoi(strtok(NULL, " "));
				}

				MeshData->GeoName = (string) Geometry->Attribute("id");
				
				Node = File.RootElement()->FirstChildElement("library_visual_scenes")->FirstChildElement("visual_scene")->FirstChildElement("node");
				while(Node != NULL)
				{
					inst = Node->FirstChildElement("instance_geometry");
					string Name = ((string) ((char *) inst->Attribute("url"))).erase(0,1);
					printf("Geo: %s   Found: %s\n",MeshData->GeoName.c_str(),Name.c_str());
					bool t = !strcmp(MeshData->GeoName.c_str(),Name.c_str());
					printf("Result: %s\n",(t)?"true":"false");
					if(!strcmp(MeshData->GeoName.c_str(),Name.c_str()))
					{
						string MatrixText = (string) Node->FirstChildElement("matrix")->GetText();
						MeshData->mMatrix = new float[16];

						(MeshData->mMatrix)[0] = atof(strtok((char*)MatrixText.c_str(), " ")); 
						for(int index=1; index<16; index++)  {(MeshData->mMatrix)[index] = atof(strtok(NULL, " "));}
						FLog("Matrix Loaded: Transpose\n");
						Node = Node->NextSiblingElement("node");
						break;
					}
					Node = Node->NextSiblingElement("node");
				}

				// Finalize tells mesh all new data is uploaded, and can begin profiling.


				Model->MeshData.push_back(MeshData);
				printf("\n*Mesh Table*\n");
				printf("Triangle C: %i\n",MeshData->mIndex.mCount/9);
				printf("Index    C: %i\n",MeshData->mIndex.mCount);
				printf("Pos      C: %i\n",MeshData->mData[0]->mCount);
				printf("Normal   C: %i\n",MeshData->mData[1]->mCount  );
				printf("TEX...   C: %i\n",MeshData->mData[2]->mCount );
				printf("TEXTURE   : %s\n\n",MeshData->mTexture.c_str());
				mesh = mesh->NextSiblingElement("mesh");

				if (mesh != NULL)
					FLog("Moving To Next Mesh");
			}


			Geometry = Geometry->NextSiblingElement("geometry");

			if (Geometry != NULL)
				FLog("Moving To Next Geometry");
		}
		FLog("*Task Complete*\n\n");

		return Model;
	}
	else
	{
		Warn("Failed to Load Model: "+string(Path),true);
		return NULL;
	}

}


};
