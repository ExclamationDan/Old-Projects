#include "ManagerRender.h"


CManagerRender::CManagerRender(void)
{
	glm::mat4 Projection = glm::perspective(90.0f, 4.0f / 3.0f, 0.1f, 100.f);
	glm::mat4 View = glm::translate(glm::mat4(1.0f),glm::vec3(0.0f, 0.0f, -25.0f));
}


CManagerRender::~CManagerRender(void)
{
}
