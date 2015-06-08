#pragma once

#include "ThirdParty\GLEW\glew.h"
#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>
#include "Util.h"

#define BUFFER_OFFSET(i) ((char *)NULL + (i))


struct OGL_Vertex 
{
	float	x,y,z,		// Vertex
			n1,n2,n3,	// Normal
			s,t;		// Texcoord
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

	vector<GLushort>	mIndex;
	vector<float>		mVertex, mNormal, mTexture;
	vector<OGL_Vertex>	mDrawData;

	void Extract_Source(CSource* Source);
	void Draw();

	CMesh();
	~CMesh();
};
