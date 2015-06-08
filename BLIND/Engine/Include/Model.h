#pragma once
#include "Mesh.h"
#include "glm\glm.hpp"

using namespace glm;

struct ModelMetaData
{
	vec3 Rotation;
	vec3 Position;

	ModelMetaData()
	{
		Rotation = vec3(0,0,0);
		Position = vec3(0,0,0);
	}
};

class CModel
{
public:
	vector<CMesh>	MeshData;

	GLuint	V,I; // Index&Data Buffers
	int		IndexSize;

	void	AddMesh(CMesh Mesh);
	void	Finalize();
	void	Draw();

	CModel(void);
	~CModel(void);
};
