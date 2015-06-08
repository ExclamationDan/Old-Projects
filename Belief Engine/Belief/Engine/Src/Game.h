#pragma once

#include <GLEW\glew.h>
#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>


#include "Util.h"
#include "FileSystem.h"
#include "EngineConfig.h"
// This is the basis of event handling, calling the base managers to call the other high level methods

class CGame
{
public:
	sf::RenderWindow	Window;
	CKeyLite			Config;
	
	void	Begin();	// Setup renderwindow and load config from XML (Data/Config/Config.xml)
	void	MainLoop(); // Where the magic happens.

	CGame(void);
	~CGame(void);
};

