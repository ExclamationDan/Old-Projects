#pragma once
//#include <GLEW\glew.h>
#include "Util.h"
#include "FileSystem.h"
#include "TinyXML\tinyxml2.h"

#include <GLEW\glew.h>
#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>

#include <iostream>
#include <string>
#include <sstream>


using namespace tinyxml2;
using namespace std;

enum MType 
{MESH_V = 0, MESH_N = 1, MESH_T = 2,MESH_INVALID = 3};



struct VertexData
{
	MType			mType;
	vector<float>	mData;
	int				mCount;
	int				mOffset;
	int				mStride;

};

struct CSource
{
	string			mID;
	vector<float>	mData;
	int				mCount;
	int				mStride;
	
	string			mType;
	int				mOffset;
};


class CMesh
{
public:
	string					GeoName;
	int						m_iTriangleCount;
	VertexData				mData[3];
	vector<int>				mIndex;
	string					mTexture; 
	vector<float>			mMatrix;

	// Mesh is no longer to hold individual elements
	// Mesh will automatically format and upload all vertex, normal, texture, ect to a VBO then reference it?

	// We will assume that every model only has one texture atlas
	// No, we will bind every texture the mesh tells us to. Don't be stupid.


	void Update_WithSource(CSource* Source)
{
	VertexData Temp;

	Temp.mType = MESH_INVALID;

	if (!(Source->mType.compare("VERTEX")))
		Temp.mType = MESH_V;
		
	if (!(Source->mType.compare("NORMAL")))
		Temp.mType = MESH_N;

	if (!(Source->mType.compare("TEXCOORD")))
		Temp.mType = MESH_T;


	if (Temp.mType != MESH_INVALID)
	{
	Temp.mData = Source->mData;
	Temp.mCount = Source->mCount;
	Temp.mOffset = Source->mOffset;
	Temp.mStride = Source->mStride;

	if (Temp.mType == MESH_V)
		{
			mData[0] = Temp;
		}
		
	if (Temp.mType == MESH_N)
		{
			mData[1] = Temp;
		}

	if (Temp.mType == MESH_T)
		{
			mData[2] = Temp;
		}
	}

}

	

	void Draw()
	{		
		

	//glPushMatrix();

	//glMultTransposeMatrixf(&mMatrix[0]);

	glBegin(GL_TRIANGLES);
	for(int i=0;i<(mIndex.size()/9)*3;i++)
	{
		// Yay for eyesores!
		//Arrays[Index[i*3+offset]*(2 or 3 )+0]
		glTexCoord2f	(mData[2].mData[mIndex[i*3+(mData[2].mOffset)]*2+0], mData[2].mData[mIndex[i*3+(mData[2].mOffset)]*2+1]);
		glVertex3f		(mData[0].mData[mIndex[i*3+(mData[0].mOffset)]*3+0], mData[0].mData[mIndex[i*3+(mData[0].mOffset)]*3+1],mData[0].mData[mIndex[i*3+(mData[0].mOffset)]*3+2]);
		glNormal3f		(mData[1].mData[mIndex[i*3+(mData[1].mOffset)]*3+0], mData[1].mData[mIndex[i*3+(mData[1].mOffset)]*3+1],mData[1].mData[mIndex[i*3+(mData[1].mOffset)]*3+2]);
	}
	glEnd();

	glPopMatrix();

	}
	

	CMesh()  {};
};


class CModel
{
public:
	vector<CMesh>	MeshData;

	// OK: Helps the manager weed out models that failed to be populated.
	bool	OK; 

	void	Draw();
	void	AddMesh(CMesh Mesh);


	CModel(void);
	~CModel(void);
};



class CLoadModel
{
protected:
	XMLElement* SourceByID(XMLElement *XMLMesh,char* ID);

	XMLElement*	ParseMesh(XMLElement *Mesh,CModel *ModelD);
	void		ParseSource(XMLElement* XMLSource,CMesh* Mesh,CSource *Source);

public:

	CModel	Load(string Path);



	CLoadModel(void);
	~CLoadModel(void);
};

