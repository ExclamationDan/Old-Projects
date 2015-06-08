#pragma once

#include <GLEW\glew.h>
#include <FreeGlut\freeglut.h>

#include "FlakPath.hpp"
#include "FlakFuncs.hpp"


#include <ThirdParty\SOIL\SOIL.h>
#include <vector>
#include <iterator>

#include "GameWindow.h"
#include "EngineConfig.h"

#define Version "0.001"
class CGame
{	
public:
	CKeyLite		 Properties;
	EngineConfig	 Config;
	GameWindow		 Window;


	void GAME_Startup(int argc, char **argv)
	{

		Properties = Config.ReadAll("Config.xml");
		Window_Setup();

		glutInit(&argc, argv);
		glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
		glutInitWindowPosition(100,100);

		glutInitWindowSize(Window.m_iHeight,Window.m_iWidth);
		Window.m_hHandle = glutCreateWindow(Properties.Getstr("Title"));

		// OpenGL init
		glEnable(GL_DEPTH_TEST);
		FLog("OpenGL Version: "+(string)((char*)glGetString(GL_VERSION)),true);
		glewInit();

	}
	
	void	Window_Setup()
		{
		Window.m_iHeight	= Properties.Geti("Height");
		Window.m_iWidth		= Properties.Geti("Width");
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

		glutSwapBuffers();
	}
	
	CGame() 
	{

	}

	~CGame() 
	{

	}
};