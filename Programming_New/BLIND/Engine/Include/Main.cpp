
#include <ThirdParty\GLEW\glew.h>

#include <SFML\Window.hpp>
#include <SFML\Graphics.hpp>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <cstdarg> // va_list for elipsis
#include <sstream>
#include <cmath>

#include "ShaderManager.h"
#include "FileSystem.h"
#include "ManagerModel.h"

#include <glm\glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>



using namespace std;

void GenericStart();
void Draw();

vector<CModel*> Models;
GLuint Prog;

float Rot;

// We can't use OpenGL BEFORE glewint();
int main(int argc, char* argv[])
{
	Rot = 0.0f;

	FSys.Setup(argv[0]);
	GenericStart();	
	return 0;
}


void ShaderPrep()
{
	ShaderManager SMan;
	Prog = SMan.LoadProgram("Shader.Vertex","Shader.Fragment");
	if (!Prog) {cout << "Shader: Failed, returned NULL." << endl;} 
}

void AddModel(string Path)
{
	CModel	*pModel = ManagerModel.Load(Path);
	if (pModel) {Models.push_back(pModel);}
}


void CanUseOpenGL()
{
	AddModel("Box.DAE");
	ShaderPrep();
}



void Draw()
{
	if (Rot > 360) {Rot = 0;}
	Rot += .03;


	glUseProgram(Prog);
	float Translate = -25.0f;

	/* Default Matrix Transform
	glm::vec3 Rotate = glm::vec3(Rot,Rot,0.0f);

	glm::mat4 Projection = glm::perspective(90.0f, 4.0f / 3.0f, 0.1f, 100.f);
	glm::mat4 ViewTranslate = glm::translate(glm::mat4(1.0f),glm::vec3(0.0f, 0.0f, Translate));

	glm::mat4 ViewRotateX = glm::rotate(ViewTranslate,Rotate.y, glm::vec3(-1.0f, 0.0f, 0.0f));

	glm::mat4 View = glm::rotate(ViewRotateX,Rotate.x, glm::vec3(0.0f, 1.0f, 0.0f));
	glm::mat4 mModel = glm::scale(glm::mat4(1.0f),glm::vec3(0.5f));

	glm::mat4 MVP = Projection * View * mModel;
	*/




	// This block is called repeatedly!
	// Z Axis problems comeing from somewhere
	Models[0]->Move.SetPos(vec3(4.0f,0.0f,0.0f));

	GLuint LocationMVP = glGetUniformLocation(Prog, "MVP");

	//glUniformMatrix4fv(LocationMVP, 1, GL_FALSE, glm::value_ptr(MVP));

	glUniformMatrix4fv(LocationMVP, 1, GL_FALSE, glm::value_ptr(Models[0]->Move.ModelViewProjection()));



	for (auto it : Models) {it->Draw();}

}

void GenericStart()
{
	sf::Window App(sf::VideoMode(800,600, 32), "Matrix Transform");

	GLenum err = glewInit();
	if (err != GLEW_OK)
		exit(1); // or handle the error in a nicer way
	if (!GLEW_VERSION_2_1)  // check that the machine supports the 2.1 API.
		exit(1); // or handle the error in a nicer way

	CanUseOpenGL();
	// Set color and depth clear value
	glClearDepth(1.f);

	glClearColor(.5f, 1.0f, 0.2f, 0.0f); 
	glClear(GL_COLOR_BUFFER_BIT); 

	// Enable Z-buffer read and write
	glEnable(GL_DEPTH_TEST);
	glDepthMask(GL_TRUE);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();

	while (App.isOpen() )
	{
		sf::Event event;
		while (App.pollEvent(event))
		{
			if (event.type == sf::Event::Closed)
				App.close();
		}


		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();

		Draw();		


		App.display();
	}

}

