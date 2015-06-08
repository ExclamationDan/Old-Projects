#pragma once
#include "Mesh.h"
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "ManagerRender.h"

using namespace glm;





// Generic Matrix Movement Class
class Movement
{
public:
	mat4	mMatrix; // Model Matrix

	vec3	vRot,vPos,vVelocity;

	Movement()
	{
		mMatrix = glm::scale(glm::mat4(1.0f),glm::vec3(0.5f));
		vRot = vPos = vVelocity = vec3(0);
	}

	void	SetPos(vec3 P)
	{	
		mMatrix = glm::scale(glm::mat4(1.0f),glm::vec3(0.5f));
		mMatrix = glm::translate(mMatrix,P);
		vPos = P;
	}

	void AddPos(vec3 P)
	{
		mMatrix = glm::translate(mMatrix,P);
		vPos += P;
	}

	// This is also AWFUL; will be rewritten into ManagerRender.
	glm::mat4	ModelViewProjection()
	{
		return manRender.mProjection * manRender.mView * mMatrix;
	}

};

class CModel
{
public:
	


	vector<CMesh>	MeshData;
	GLuint	V,I; // Index&Data Buffers
	int		IndexSize;

	Movement	Move;


	void	AddMesh(CMesh Mesh);
	void	Finalize();
	void	Draw();

	CModel(void);
	~CModel(void);
};
