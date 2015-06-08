#pragma once
#include <GLEW\glew.h>
#include "FlakFuncs.hpp"
#include <vector>


enum MType {Vertex = 0, V = 0, Normal = 1, N = 1, Texcoord = 2, Te = 2,Tex = 2,Color = 3, Colour = 3, C = 3 };


struct IndexData
{
	int* mData;
	int	 mCount;
	~IndexData()
	{ if (mData) delete[] mData; }
};

struct VertexData
{
	MType   mType;
	float*  mData;
	int		mCount;
	int		mOffset;
	int		mStride;
	~VertexData() { if (mData) delete[] mData; }
};

struct Vertex
{
float x, y, z;        
float nx, ny, nz;           
float s, t;               
};

struct CSource
{
	string		mID;
	float*		mData;
	int			mCount;
	int			mStride;
	
	char*	    mType;
	int			mOffset;
};

struct	Identity
{
	int	mBufferStart;
	int mVertexOffset;
	int mNormalOffset;
	int mTextureOffset;
};

class CMesh
{
public:
	string					GeoName;

	VertexData*				mData[3];
	IndexData				mIndex;
	string					mTexture; 
	float*					mMatrix;

	// Mesh is no longer to hold individual elements
	// Mesh will automatically format and upload all vertex, normal, texture, ect to a VBO then reference it.

	// We will assume that every model only has one texture atlas


	void Update_WithSource(CSource* Source)
{
	VertexData *Temp;
	Temp = new VertexData;

	if (!(strcmp(Source->mType,"VERTEX")))
		Temp->mType = V;
		
	if (!(strcmp(Source->mType,"NORMAL")))
		Temp->mType = N;

	if (!(strcmp(Source->mType,"TEXCOORD")))
		Temp->mType = Tex;

	if (!(strcmp(Source->mType,"COLOR")) || !(strcmp(Source->mType,"COLOUR")))
		Temp->mType = C;

	Temp->mData = Source->mData;
	Temp->mCount = Source->mCount;
	Temp->mOffset = Source->mOffset;
	Temp->mStride = Source->mStride;

	if (Temp->mType == V)
		{
			mData[0] = Temp;
		}
		
		if (Temp->mType == N)
		{
			mData[1] = Temp;
		}

		if (Temp->mType == Te)
		{
			mData[2] = Temp;
		}

		if (Temp->mType == C)
		{
			mData[3] = Temp;
		}
}

	

	void Draw()
	{		
		
	glPushMatrix();
	glMultTransposeMatrixf(mMatrix);

	glBegin(GL_TRIANGLES);
	for(int i=0;i<(mIndex.mCount/9)*3;i++)
	{
		// Yay for eyesores!
		//Arrays[Index[i*3+offset]*(2 or 3 )+0]
		glTexCoord2f	(mData[2]->mData[mIndex.mData[i*3+(mData[2]->mOffset)]*2+0], mData[2]->mData[mIndex.mData[i*3+(mData[2]->mOffset)]*2+1]);
		glVertex3f		(mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+0], mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+1],mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+2]);
		glNormal3f		(mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+0], mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+1],mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+2]);
	}
	glEnd();

	glPopMatrix();

	}


	CMesh(void)  {};
	~CMesh(void) {if (mData){delete [] mData;}};
};






/*
enum MType {Vertex = 0, V = 0, Normal = 1, N = 1, Texcoord = 2, Te = 2,Tex = 2,Color = 3, Colour = 3, C = 3 };


struct IndexData
{
	int* mData;
	int	 mCount;
	~IndexData()
	{ if (mData) delete[] mData; }
};

struct VertexData
{
	MType   mType;
	float*  mData;
	int		mCount;
	int		mOffset;
	int		mStride;
	~VertexData() { if (mData) delete[] mData; }
};

struct Vertex
{
float x, y, z;        
float nx, ny, nz;           
float s, t;               
};

struct CSource
{
	string		mID;
	float*		mData;
	int			mCount;
	int			mStride;
	
	char*	    mType;
	int			mOffset;
};


class CMesh
{
public:
	string					GeoName;

	VertexData*				mData[3];
	IndexData				mIndex;
	string					mTexture; 
	float*					mMatrix;

	// Mesh is no longer to hold individual elements
	// Mesh will automatically format and upload all vertex, normal, texture, ect to a VBO then reference it.

	// We will assume that every model only has one texture atlas


	void Update_WithSource(CSource* Source)
{
	VertexData *Temp;
	Temp = new VertexData;

	if (!(strcmp(Source->mType,"VERTEX")))
		Temp->mType = V;
		
	if (!(strcmp(Source->mType,"NORMAL")))
		Temp->mType = N;

	if (!(strcmp(Source->mType,"TEXCOORD")))
		Temp->mType = Tex;

	if (!(strcmp(Source->mType,"COLOR")) || !(strcmp(Source->mType,"COLOUR")))
		Temp->mType = C;

	Temp->mData = Source->mData;
	Temp->mCount = Source->mCount;
	Temp->mOffset = Source->mOffset;
	Temp->mStride = Source->mStride;

	if (Temp->mType == V)
		{
			mData[0] = Temp;
		}
		
		if (Temp->mType == N)
		{
			mData[1] = Temp;
		}

		if (Temp->mType == Te)
		{
			mData[2] = Temp;
		}

		if (Temp->mType == C)
		{
			mData[3] = Temp;
		}
}

	

	void Draw()
	{		
		
	glPushMatrix();
	glMultTransposeMatrixf(mMatrix);

	glBegin(GL_TRIANGLES);
	for(int i=0;i<(mIndex.mCount/9)*3;i++)
	{
		// Yay for eyesores!
		//Arrays[Index[i*3+offset]*(2 or 3 )+0]
		glTexCoord2f	(mData[2]->mData[mIndex.mData[i*3+(mData[2]->mOffset)]*2+0], mData[2]->mData[mIndex.mData[i*3+(mData[2]->mOffset)]*2+1]);
		glVertex3f		(mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+0], mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+1],mData[0]->mData[mIndex.mData[i*3+(mData[0]->mOffset)]*3+2]);
		glNormal3f		(mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+0], mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+1],mData[1]->mData[mIndex.mData[i*3+(mData[1]->mOffset)]*3+2]);
	}
	glEnd();

	glPopMatrix();

	}


	CMesh(void)  {};
	~CMesh(void) {if (mData){delete [] mData;}};
};
*/