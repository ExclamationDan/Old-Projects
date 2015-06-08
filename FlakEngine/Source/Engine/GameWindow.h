#pragma once

#include <GLEW\glew.h>


#include "FlakPath.hpp"
#include "FlakFuncs.hpp"


#include <vector>
#include <iterator>



class GameWindow
{
public:
	GLuint	m_hHandle;
	int		m_iHeight;
	int		m_iWidth;
	char*	m_cTitle;

	
	static void WINDOW_Resize(int w, int h) 
	{

		h = ((h<50)*50)+h;
		w = ((w<50)*50)+w;

		float ratio = w * 1.0 / h;

		// Use the Projection Matrix
		glMatrixMode(GL_PROJECTION);

		// Reset Matrix
		glLoadIdentity();

		// Set the viewport to be the entire window
		glViewport(0, 0, w, h);

		// Set the correct perspective.
		gluPerspective(45.0f, ratio, 0.1f, 100.0f);

		// Get Back to the Modelview
		glMatrixMode(GL_MODELVIEW);
}


	GameWindow(void)
	{
	}

	~GameWindow(void)
	{
	}
};

