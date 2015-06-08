#pragma once
#include "FlakFuncs.hpp"
#include "Mesh.hpp"

#include <ThirdParty\SOIL\SOIL.h>
#include <vector>
#include <iterator>


// Model will be the main container for mesh data.
// ENTITY will hold a pointer to a drawable model, along with simple draw properties, such as matrix, position, and so on.

class CModel
{
private:

public:
	vector<GLuint>	MeshReference;

	vector<CMesh*> MeshData;
	vector<CMesh*>::iterator it;

	void Render()
	{
		for (it = MeshData.begin();it != MeshData.end();it++)
		{
			(*it)->Draw();
		}
	}


	CModel() {}
	~CModel() 
	{
	// Unloading is called by sending a request to the Resource Manager
	}
};

