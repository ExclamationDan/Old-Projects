#include "Model.h"


CModel::CModel(void)
{
}

CModel::~CModel(void)
{
}

void CModel::Draw()
{
	//for (auto it : MeshData)
		//it.Draw();
	glBindBuffer(GL_ARRAY_BUFFER, V);
	glEnableVertexAttribArray(0);glEnableVertexAttribArray(1);glEnableVertexAttribArray(2);

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,sizeof(OGL_Vertex), BUFFER_OFFSET(0));
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,sizeof(OGL_Vertex), BUFFER_OFFSET(12));
	glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,sizeof(OGL_Vertex), BUFFER_OFFSET(24));


	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, I);
	glDrawElements(GL_TRIANGLES, IndexSize,GL_UNSIGNED_SHORT, BUFFER_OFFSET(0));

	glDisableVertexAttribArray(0);glDisableVertexAttribArray(1);glDisableVertexAttribArray(2);
}

void CModel::AddMesh(CMesh XMLMesh)
{
	MeshData.push_back(XMLMesh);
}

void CModel::Finalize()
{
	vector<OGL_Vertex>	Verts;
	vector<GLushort>	Index;
	
	for (auto it = MeshData.begin(); it != MeshData.end(); it++) {Verts.insert(Verts.end(), it->mDrawData.begin(),it->mDrawData.end());}

	Index = CreateIndexVector(Verts.size());
	IndexSize = Verts.size();
	
	// We're done with all those filthy meshes.
	MeshData.clear();

	glGenBuffers(1, &V);
	glGenBuffers(1, &I);

	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, I);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, IndexSize*sizeof(GLushort), &Index[0], GL_STATIC_DRAW);

	glBindBuffer(GL_ARRAY_BUFFER, V);
	glBufferData(GL_ARRAY_BUFFER,sizeof(OGL_Vertex)*Verts.size(), &Verts[0], GL_STATIC_DRAW);

}