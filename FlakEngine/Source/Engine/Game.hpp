#pragma once

#include <SFML\Graphics.hpp>
#include <GLEW\glew.h>

#include "FlakPath.hpp"
#include "FlakFuncs.hpp"

#include <vector>
#include <iterator>

#include "GameWindow.h"
#include "EngineConfig.h"

#define Version "0.001"

using namespace std;


class CGame
{	
public:
	EngineConfig		CParser;
	CKeyLite			Config;
	sf::RenderWindow	window;


	void GAME_Startup(int argc, char **argv)
	{
		
		Config = CParser.ReadAll("Config.xml");
		sf::RenderWindow	window(sf::VideoMode(Config.Geti("Height"), Config.Geti("Width")), Config.Getstr("Title"));

		// OpenGL init
		//glEnable(GL_DEPTH_TEST);
		//FLog("OpenGL Version: "+(string)((char*)glGetString(GL_VERSION)),true);


	}
	



	static void GAME_Render()
	{
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glClearColor(0.0f,0.5f,0.8f,0);
		// Reset transformations
		glLoadIdentity();

		// Set the camera
		//gluLookAt(	x, 1.0f, z,x+lx, 1.0f, z+lz,0.0f, 1.0f, 0.0f);
		//glColor3f(0.0f,0.4f,0.6f);
		//SimpleRender();

		glColor3f(0.9f, 0.9f, 0.9f);
		glBegin(GL_QUADS);
		glVertex3f(-100.0f, 0.0f, -100.0f);
		glVertex3f(-100.0f, 0.0f, 100.0f);
		glVertex3f( 100.0f, 0.0f, 100.0f);
		glVertex3f( 100.0f, 0.0f, -100.0f);
		glEnd();


	}
	
	CGame() 
	{

	}

	~CGame() 
	{

	}
};