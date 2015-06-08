#pragma once
#include <GLEW\glew.h>
#include <ThirdParty\SOIL\SOIL.h>
#include "FlakPath.hpp"
#include "FlakFuncs.hpp"
#include <map>

#include "Buffer.hpp"


class CResourceManager
{
private:
	
	int Buffer_Size; // In bytes (4mb is standard)

	void Startup()
	{
		int Buffer_Size = 4194304;

	}
	struct Texture
		{
			GLuint*		mTexture;
			int			mCount;
			Texture() {mCount = 0;}
		};


	// Bufferpack handles only size management, everything else is something else's job.
	struct BufferPack
	{
		GLuint*	mBuffer;
		int		mCurrentSize;
		int		mCapacity;
	};

	map<string,Texture>				mTextures;
	map<string,Texture>::iterator	mT;




	GLuint* Texture_RawBind(string Path)
	{
		GLuint tex_ID;
		tex_ID = SOIL_load_OGL_texture(
			Path.c_str(),
			SOIL_LOAD_AUTO,
			SOIL_CREATE_NEW_ID,
			SOIL_FLAG_POWER_OF_TWO
			| SOIL_FLAG_MIPMAPS
			| SOIL_FLAG_MULTIPLY_ALPHA
			| SOIL_FLAG_COMPRESS_TO_DXT
			| SOIL_FLAG_DDS_LOAD_DIRECT
			| SOIL_FLAG_INVERT_Y
			);

		if( tex_ID > 0 )
		{
			glBindTexture( GL_TEXTURE_2D, tex_ID );
			return &tex_ID;
		}
		else
		{
			Warn("ResourceManager - Failed To Load Texture File: "+Path,true);
			return 0;
		}

	}


public:

	// Rules:
	// A resource must be logged
	// A logged resource must be refrenced rather than re-allocated
	// Unlogged resources must be logged and allocated
	// All mesh, model, and texture loading should be passed through the resource manager
	// Generic or raw information may only be logged, such as vertex data. Position, and other dynamic data must be handled outside the resource manager.
	// logged data is relative to file path, including file name. ( Folder/Bill.jpg != Folder11/Bill.jpg )
	// It is up to modelers to use the same texture atlas for multiple (similar) models to enhance preformance.
	// The resource handler will sort models by the most common occurance of texture atlases. As to lower the amount of texture binding from entity to entity.

	// All models must be destroyed from memory here, as to check if their texture atlas and other data is to be de-allocated. (if there are multiple occurances of the item, data will be maintained)
	// The model class will only contain a pointer to a set of VBO's to draw it's mesh data.

	GLuint*	Texture_Get(string Path)
	{
		mT=mTextures.find(Path);
		if (mT != mTextures.end())
		{
			FLog("ResourceManager: Returned Pre-Allocated Path");
			(*mT).second.mCount += 1;
			return (*mT).second.mTexture;
		}
		else
		{
			FLog("ResourceManager: Created New Resource Reference");
			GLuint*	Test = Texture_RawBind(Path);

			if (Test != 0)
			{
				mTextures[Path].mTexture = Test;
				mTextures[Path].mCount += 1;
				return Test;
			}

			else
			{
				Warn("ResourceManager - Failed To Load Texture File: "+Path,true);
				return 0;
			}
		}

	}


	CResourceManager(void)  
	{
		Startup();
	
	};
	~CResourceManager(void) {};
};

static CResourceManager RManager;