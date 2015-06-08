#include "Game.h"
#include "LoadModel.h"

CGame::CGame(void)
{
}


CGame::~CGame(void)
{
}

void	CGame::Begin()
{


	EngineConfig	EConfig;
	Config = EConfig.ReadAll("Config.xml");

	Window.Create(sf::VideoMode(Config.Geti("Width"),Config.Geti("Height"), 32),Config.Getstr("Title"));

	 // Set color and depth clear value
    glClearDepth(1.f);
    glClearColor(0.f, 0.f, 0.f, 0.f);

    // Enable Z-buffer read and write
    glEnable(GL_DEPTH_TEST);
    glDepthMask(GL_TRUE);

    // Setup a perspective projection
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(90.f, 1.f, 1.f, 500.f);

	
	MainLoop();

}

void	CGame::MainLoop()
{
	CLoadModel MLoad;
	CModel Model = MLoad.Load("square.DAE");
	while (Window.IsOpened() )
    {
        sf::Event Event;
		while (Window.GetEvent(Event))
		{
            if (Event.Type == sf::Event::Closed) 
			{
				Window.Close();
			}

			if (Event.Type == sf::Event::Resized)
			{
				 glViewport(0, 0, Event.Size.Width, Event.Size.Height);
			}
		}         


		Model.Draw();
	Window.Display();

    }
}

