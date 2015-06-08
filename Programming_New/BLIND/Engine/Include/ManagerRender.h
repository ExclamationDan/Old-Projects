#pragma once

#include <GLEW\glew.h>
#include "ShaderManager.h"
#include "ManagerModel.h"


class CManagerRender
{
public:
	mat4 mProjection,mView;


	CManagerRender(void);
	~CManagerRender(void);



};

static CManagerRender manRender;