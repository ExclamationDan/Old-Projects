#pragma once
#include <gl\glew.h>
#include "ResourceManager.hpp"


class CRenderManager
{
private:


public:

	// Rules:
	// Rendering should only occur near a point of interest, such as a camera displaying part of the map or the player's fov
	// Screen effects may be displayed on any screen, be it a camera or the player's viewport
	// This manager relies on the Resource manager.
	// This manager is to request an optimized list from the Resource Manager, draw them with a varety of settings, then repeat.
	// Entitites with the same model will be rendered one after another (10 houses) rather than (house, car, house, misc, house, misc...)


	CRenderManager(void)  {};
	~CRenderManager(void) {};
};

static CResourceManager RManager;