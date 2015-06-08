#include "Mesh.h"


CMesh::CMesh(void)
{

}


CMesh::~CMesh(void)
{

}


void	CMesh::Extract_Source(CSource *Source)
{

		if (!(Source->mType.compare("VERTEX")))			
		{mVertex = Source->mData;}

		if (!(Source->mType.compare("NORMAL")))	
		{mNormal = Source->mData;}

		if (!(Source->mType.compare("TEXCOORD")))	
		{mTexture = Source->mData;}


		if ( (!(mVertex.empty()) && !(mNormal.empty()) && !(mTexture.empty())))
		{

			vector<GLushort> NewIndex;

			for (int i = 0;mIndex.size() > i;)
			{
				OGL_Vertex Final;
				Final.x = mVertex[mIndex[i]*3];
				Final.y = mVertex[mIndex[i]*3+1];
				Final.z = mVertex[mIndex[i]*3+2];

				Final.n1 = mNormal[mIndex[i+1]*3];
				Final.n2 = mNormal[mIndex[i+1]*3+1];
				Final.n3 = mNormal[mIndex[i+1]*3+2];

				Final.s = mTexture[mIndex[i+2]*2];
				Final.t = mTexture[mIndex[i+2]*2+1];

				mDrawData.push_back(Final);
				NewIndex.push_back(i/3);
				if (i == 0) {i = 3;} else {i+=3;}
			}
			mIndex = NewIndex;
		}


}

