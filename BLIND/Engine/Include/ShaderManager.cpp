#include "ShaderManager.h"


ShaderManager::ShaderManager(void)
{

}


ShaderManager::~ShaderManager(void)
{
}


string ShaderManager::File_Load(string Name)
{
	ifstream File(FSys.AliasAdd("Root",Name));
	if(!File)
	{
		return string ("FAIL_READ");
	}

	stringstream Data;
	Data << File.rdbuf();
	File.close();
	return Data.str();
}


bool	ShaderManager::File_Exists(string Name)
{
	ifstream File;

	File.open(FSys.AliasAdd("Root",Name));
	if (File.is_open())
	{	
		File.close();
		return true;
	}
	else
	{
		return false;
	}

}


GLuint  ShaderManager::LoadShader(string Path,GLenum Type)
{
	if (!File_Exists(Path))
	{
		cout << "Failed to load Shader File.\n";
		return (GLuint) NULL;
	}

	GLint  Test;

	string		ShaderData = File_Load(Path);
	GLuint		Shader = glCreateShader(Type);
	
	GLint		ShaderLen = ShaderData.size();
	const char*	ShaderSource = ShaderData.c_str();

	glShaderSource(Shader,1,&ShaderSource,(GLint*) &ShaderLen);
	glCompileShader(Shader);

	cout << "Shader: Error Checking...\n";
	glGetShaderiv(Shader,GL_COMPILE_STATUS,&Test);
	if ( Test == GL_FALSE)
	{
		char Log[1024];
		glGetShaderInfoLog(Shader,1024,NULL,Log);
		cout << "Shader: "<< Shader <<" Failed With the Following Log:\n" << Log << "Shader: Failure.\n\n";
		glDeleteShader(Shader);
		return (GLuint) NULL;
	}
	cout << "Shader: Success.\n";
	return Shader;



}

GLuint	ShaderManager::LoadProgram(string Vertex,string Fragment)
{
	GLuint	hVertex		= LoadShader(Vertex,GL_VERTEX_SHADER);
	GLuint	hFragment	= LoadShader(Fragment,GL_FRAGMENT_SHADER);
	GLuint	hReturn;
	GLint	Test;

	if ( (hVertex == NULL) || (hFragment == NULL) )
	{
		cout << "LoadShaders: Failed to Load One or More Shader Files.\n";
		return (GLuint) NULL;
	}

	cout << "Creating Program...\n";
	hReturn = glCreateProgram();

	cout << "Attaching...\n";
	glAttachShader(hReturn,hVertex);
	glAttachShader(hReturn,hFragment);

	cout << "Binding Attributes...\n";
	// 0 = Position, 1 = Color, 2 = Normal;
	glBindAttribLocation(hReturn,0,"vertex");
	//glBindAttribLocation(hReturn,1,"vFragColor");
	

	cout << "Linking...\n";
	glLinkProgram(hReturn);

	cout << "Error Checking...\n";
	glGetProgramiv(hReturn,GL_LINK_STATUS,&Test);
	if (Test == GL_FALSE)
	{
		char Log[1024];
		glGetProgramInfoLog(hReturn,1024,NULL,Log);
		cout << "Program Failed with Error Log:\n" << Log << endl;
		glDeleteProgram(hReturn);
		return (GLuint) NULL;
	}

	cout << "Returning...\n";
	return hReturn;



}