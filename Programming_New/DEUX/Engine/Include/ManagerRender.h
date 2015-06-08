#pragma once

#include <GLEW\glew.h>
#include "ShaderManager.h"
#include "ManagerModel.h"
#include <glm/glm.hpp>



class CManagerRender
{
public:
	glm::mat4 mProjection,mView;

	CManagerRender(void);
	~CManagerRender(void);
};

static CManagerRender manRender;