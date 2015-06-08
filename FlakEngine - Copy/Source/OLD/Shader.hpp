#pragma once
#include <GLEW\glew.h>
#include <stdio.h>

#include "FlakPath.hpp"
#include "FlakFuncs.hpp"



using namespace std;

// This will be a very strict implementation
// The work is done on link, so it doesn't matter how many times we attach a shader.

/*
class ShaderManager
{
	struct FlakShader
	{
		GLuint mShader;
		GLenum mType;
		bool loaded;
		FlakShader()
		{
			//Warn("Shader: Created To Non-Uniform Standards!");
			loaded = false;
		}

		void Load(GLenum Type, string Path)
		{
			loaded = true;
			mShader = glCreateShader(Type);
			string temp = FPath.File_Read_Aliased("Data",Path);
			const GLchar* Data = (const GLchar*) temp.c_str();
			GLint Len = temp.length(); 
			glShaderSource(mShader, 1, &Data, &Len);
			glCompileShader(mShader);
		}

		FlakShader(GLenum Type, string Path)
		{
			Load(Type,Path);
		}

		void Attach(GLuint Program)
		{
			if (!loaded)
			{
				Warn("Shader: Attempted to attach an unloaded and compiled shader!",true);
			}
			else
				glAttachShader(Program,mShader);

		}

	};

	struct FlakProgram
	{
		string Name;
		GLuint mProgram;
		FlakShader Vert,Frag;


		FlakProgram() {Name = "NONE";}
		FlakProgram(string VertPath, string FragPath)
		{
			Load(VertPath,FragPath);
		}

		void Load(string VertPath, string FragPath)
		{
			mProgram = glCreateProgram();
			Vert.Load(GL_VERTEX_SHADER,VertPath);
			Frag.Load(GL_FRAGMENT_SHADER,FragPath);
		}

		void Link()
		{
			Vert.Attach(mProgram);
			Frag.Attach(mProgram);
			glLinkProgram(mProgram);
			GLint linked;
			glGetProgramiv(mProgram, GL_LINK_STATUS, &linked);
			if (!linked)
			{Warn("Shader(s) Failed To Link To Program!",true);} 

		}
		void Use()
		{
			glUseProgram(mProgram);
		}

		void Finalize()
		{
			Link();
			Use();
		}

		~FlakProgram()
		{
			if(glIsProgram(mProgram))
			{
				glDeleteProgram(mProgram);
			}
		}
	};

	struct Shader_PathPair

	{
		string Vertex,Fragment;
	};

public:
	map<string,Shader_PathPair> ShaderPaths;
	FlakProgram *mProgram;

	ShaderManager()  
	{
		Create_ShaderList();
	}
	~ShaderManager(void)   {};

	void Switch(string Name = "Default")
	{
		map<string,Shader_PathPair>::iterator it;
		it = ShaderPaths.find(Name);

		if ( it != ShaderPaths.end() )
		{
			// If strings are NOT equal ( 0 means strings are equal)

			if (mProgram)
			{
				if (mProgram->Name.compare(Name))
				{
					// Deconstructors should handle any violation errors
					delete mProgram;
					mProgram = new FlakProgram();
					mProgram->Load((string) ShaderPaths[Name].Vertex,(string) ShaderPaths[Name].Fragment);
					mProgram->Name = Name;
					mProgram->Use();
				}
			}
			else
			{
				mProgram = new FlakProgram();
				mProgram->Load((string) ShaderPaths[Name].Vertex,(string) ShaderPaths[Name].Fragment);
				mProgram->Name = Name;
				mProgram->Finalize();
			}

		}
		else
		{
			Warn("Shader: Failure to Locate ShaderXML Pair: "+(string)Name);
		}
		Debug(mProgram->mProgram);
	}

	void Create_ShaderList()
	{
		TiXmlDocument File(FPath.Dir_Add_Aliased("Config","ShaderPairs.XML").c_str());

		if (File.LoadFile())
		{
			TiXmlElement* Pair,*Shader;  Shader_PathPair SPPair;
			Pair = File.RootElement()->FirstChildElement("Pair");
			while(Pair != NULL)
			{	
				Shader = Pair->FirstChildElement("Shader");
				while (Shader != NULL)
				{
					if (strcmp(Shader->Attribute("Type"),"Fragment") == 0) {SPPair.Fragment = (string) Shader->Attribute("Path");}
					if (strcmp(Shader->Attribute("Type"),"Vertex")   == 0) {SPPair.Vertex   = (string) Shader->Attribute("Path");}
					Shader = Shader->NextSiblingElement("Shader");
				}
				ShaderPaths[(string)Pair->Attribute("Name")] = SPPair;
				FLog("Shader: Added Profile - "+(string)Pair->Attribute("Name"));
				Pair = Pair->NextSiblingElement("Pair");

			}
		}
		else
		{Warn("Could not load 'shaderpairs.xml'!",true);}
		//PrintPaths();
	}

	void PrintPaths()
	{
		for (map<string,Shader_PathPair>::iterator it = ShaderPaths.begin(); it != ShaderPaths.end(); it++)
		{printf("\n Name: %s \n Vert: %s \n Frag: %s \n\n",(*it).first,(*it).second.Vertex,(*it).second.Fragment);}
	}

	void Debug(GLuint Object)
	{
		int logLength = 0;
		int maxLength;

		if(glIsShader(Object))
			glGetShaderiv(Object,GL_INFO_LOG_LENGTH,&maxLength);
		else
			glGetProgramiv(Object,GL_INFO_LOG_LENGTH,&maxLength);

		char infoLog[1000];

		if (glIsShader(Object))
			glGetShaderInfoLog(Object, maxLength, &logLength, infoLog);
		else
			glGetProgramInfoLog(Object, maxLength, &logLength, infoLog);

		if (logLength > 0)
			Warn(infoLog,true);
	}

};
*/