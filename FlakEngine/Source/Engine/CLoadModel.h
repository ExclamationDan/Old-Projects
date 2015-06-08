#pragma once
#include "TinyXML\tinyxml2.h"

using namespace std;
using namespace tinyxml2;

class CLoadModel
{
public:

	// Parse | ParseRoot | ParseMeta
	// CModel CMesh CVector3? CVector2?
	CModel	LoadModel(char* Path);

	void	ParseSource();

	CLoadModel(void);
	~CLoadModel(void);
};

