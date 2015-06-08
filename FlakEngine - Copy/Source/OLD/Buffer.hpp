#pragma once
#include <GLEW\glew.h>
#include "FlakFuncs.hpp"
#include <vector>
#include <iterator>



class CBuffer
{
private:

public:

	GLuint		mBuffer;
	GLenum		mType;

	void	B_Gen() 
	{
		mType = GL_VERTEX_ARRAY;
		glGenBuffers(1,&mBuffer);
	}

	void	B_Bind(GLenum BufferType) 
	{
		glBindBuffer(BufferType,mBuffer); 
		mType = BufferType;
	}

	void	B_Bind() 
	{
		glBindBuffer(mType,mBuffer); 
	}

	void	B_Data(int Size, const void* Data, GLenum Usage = GL_STATIC_DRAW)
	{
		B_Bind();
		glBufferData(mType, Size, Data, Usage);
	}

	void	B_SubData(int OffSet,int Size, const void *Data)
	{
		B_Bind();
		glBufferSubData(mType,OffSet,Size,Data);
	}

	void	B_MapRange(int OffSet,int Length, GLbitfield AccessFlags)
	{
		B_Bind();
		glMapBufferRange(mType, OffSet, Length, AccessFlags);
	}

	CBuffer(bool Generate = true) 
	{
		if (Generate) 
			B_Gen();
	}

	CBuffer(GLenum BufferType) 
	{
		B_Gen();
		B_Bind(BufferType);
	}



	~CBuffer() {}	
};


	bool B_ComplianceTest()
{
	FLog("\n\nBuffer Compliancy Test: \n",true);
	FLog("\nUploaded Test Data Consists of 1, 2, 3, 4, 5. \n",true);
	int TestData[] = {1,2,3,4,5};
	int *Data;
	CBuffer Buffer;
	Buffer.B_Bind();

	if(!Test_StandardReturn(glIsBuffer(Buffer.mBuffer),"Buffer Registered"))
	{
		Warn("Buffer Test Critical Failure; Buffer Not Registered.\nBuffer Test Exited.",true);
		return false;
	}
	
	Buffer.B_Data(5*sizeof(int),TestData);
	glGetBufferSubData(Buffer.mType,NULL,5*sizeof(int),Data);
	Test_StandardReturn((Data[4] == 5.0f),"Buffer Data Upload ");
	cout << Data[1] << endl;

	FLog("Buffer Compliancy Test Complete.\n",true);
	return true;

}