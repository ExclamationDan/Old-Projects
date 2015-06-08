#pragma once

#include <ThirdParty\GLEW\glew.h>

#include "FileSystem.h"
#include <iostream>
#include <stdio.h>
#include <cstdarg>
#include <vector>
#include <fstream>
#include <sstream>

using namespace std;

class ShaderManager
{
private:
	GLuint LoadShader(string Path,GLenum Type);

public:
	ShaderManager(void);
	~ShaderManager(void);

	string	File_Load(string Path);
	bool	File_Exists(string Path);

	GLuint LoadProgram(string Vertex,string Fragment);

};


class shader_prog {
    GLuint vertex_shader, fragment_shader, prog;

    template <int N>
    GLuint compile(GLuint type, char const *(&source)[N]) {
        GLuint shader = glCreateShader(type);
        glShaderSource(shader, N, source, NULL);
        glCompileShader(shader);
        GLint compiled;
        glGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);
        if (!compiled) {
            GLint length;
            glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &length);
            std::string log(length, ' ');
            glGetShaderInfoLog(shader, length, &length, &log[0]);
            throw std::logic_error(log);
            return false;
        }
        return shader;
    }
public:
    template <int N, int M>
    shader_prog(GLchar const *(&v_source)[N], GLchar const *(&f_source)[M]) {
        vertex_shader = compile(GL_VERTEX_SHADER, v_source);
        fragment_shader = compile(GL_FRAGMENT_SHADER, f_source);
        prog = glCreateProgram();
        glAttachShader(prog, vertex_shader);
        glAttachShader(prog, fragment_shader);
        glLinkProgram(prog);
    }

    operator GLuint() { return prog; }
    void operator()() { glUseProgram(prog); }

    ~shader_prog() {
        glDeleteProgram(prog);
        glDeleteShader(vertex_shader);
        glDeleteShader(fragment_shader);
    }
};