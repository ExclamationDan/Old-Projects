#include "Game.hpp"

CGame *Game;

void main(int argc, char **argv) 
{
	Game = new CGame();	
	Game->GAME_Startup(argc,argv);
	glutDisplayFunc (Game->GAME_Render);
	glutIdleFunc	(Game->GAME_Render);
	glutReshapeFunc (Game->Window.WINDOW_Resize);
	EngineConfig Config;

	glutMainLoop();
}





//#include <GLEW\glew.h>
//#include <FreeGlut\freeglut.h>
//
//#include "FlakPath.hpp"
//
//#include "Shader.hpp"
//#include "FlakFuncs.hpp"
//#include "ColladaLoader.hpp"
//
//#include "ResourceManager.hpp"
//
//
//
////ShaderManager SManager;
//
//
//Collada Loader;
//
//CModel *Model;
//
//GLuint WindowHandle;
//GLfloat ambientLight[] = { 1.0f, 1.0f, 1.0f, 1.0f };
//GLfloat lightPos[] = { -75.0f, 150.0f, -50.0f, 0.0f };
//
//float angle=0.0;
//float lx=0.0f,lz=-1.0f;
//float x=0.0f,z=5.0f;
//float deltaAngle = 0.0f;
//int xOrigin = -1;
//
//
//void SimpleLoad();
//void SimpleRender();
//
//void drawsphere() 
//{
//	glColor3f(1.0f, 0.8f, 0.4f);
//	glTranslatef(0.0f ,0.75f, 0.0f);
//	glutSolidSphere(0.75f,20,20);
//}
//
//void Resize(int w, int h) {
//
//	if (h == 0)
//		h = 1;
//	float ratio = w * 1.0 / h;
//
//	// Use the Projection Matrix
//	glMatrixMode(GL_PROJECTION);
//
//	// Reset Matrix
//	glLoadIdentity();
//
//	// Set the viewport to be the entire window
//	glViewport(0, 0, w, h);
//
//	// Set the correct perspective.
//	gluPerspective(45.0f, ratio, 0.1f, 100.0f);
//
//	// Get Back to the Modelview
//	glMatrixMode(GL_MODELVIEW);
//}
//
//void NKeys(unsigned char key, int x, int y) 
//{
//	if (key == 27)
//		exit(0);
//}
//void SKeys(int key, int xx, int yy) {
//
//	float fraction = 0.3f;
//
//	switch (key) {
//	case GLUT_KEY_LEFT :
//		angle -= 0.01f;
//		lx = sin(angle);
//		lz = -cos(angle);
//		break;
//	case GLUT_KEY_RIGHT :
//		angle += 0.01f;
//		lx = sin(angle);
//		lz = -cos(angle);
//		break;
//	case GLUT_KEY_UP :
//		x += lx * fraction;
//		z += lz * fraction;
//		break;
//	case GLUT_KEY_DOWN :
//		x -= lx * fraction;
//		z -= lz * fraction;
//		break;
//
//	case GLUT_KEY_HOME:
//		SOIL_save_screenshot("Screenshot.jpg",SOIL_SAVE_TYPE_BMP,0, 0, 300, 300);
//		break;
//	}
//}
//
//void MButton(int button, int state, int x, int y) {
//
//	// only start motion if the left button is pressed
//	if (button == GLUT_LEFT_BUTTON) {
//
//		// when the button is released
//		if (state == GLUT_UP) {
//			angle += deltaAngle;
//			xOrigin = -1;
//		}
//		else  {// state = GLUT_DOWN
//			xOrigin = x;
//		}
//	}
//}
//void MMove(int x, int y) {
//
//	// this will only be true when the left button is down
//	if (xOrigin >= 0) {
//
//		// update deltaAngle
//		deltaAngle = (x - xOrigin) * 0.004f;
//
//		// update camera's direction
//		lx = sin(angle + deltaAngle);
//		lz = -cos(angle + deltaAngle);
//	}
//}
//
//void Render(void) 
//{
//	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
//	glClearColor(0.0f,0.5f,0.8f,0);
//	// Reset transformations
//	glLoadIdentity();
//
//	// Set the camera
//	gluLookAt(	x, 1.0f, z,x+lx, 1.0f, z+lz,0.0f, 1.0f, 0.0f);
//	glColor3f(0.0f,0.4f,0.6f);
//	SimpleRender();
//
//
//	glColor3f(0.9f, 0.9f, 0.9f);
//	glBegin(GL_QUADS);
//	glVertex3f(-100.0f, 0.0f, -100.0f);
//	glVertex3f(-100.0f, 0.0f, 100.0f);
//	glVertex3f( 100.0f, 0.0f, 100.0f);
//	glVertex3f( 100.0f, 0.0f, -100.0f);
//	glEnd();
//
//
//	glutSwapBuffers();
//}
//
//void main(int argc, char **argv) 
//{
//	
////#pragma comment( linker, "/subsystem:\"windows\" /entry:\"mainCRTStartup\"" ) // Hide Console
//
//	FLog("--- FlakEngine Start ---",true);
//
//	glutInit(&argc, argv);
//
//
//	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
//	glutInitWindowPosition(100,100);
//	glutInitWindowSize(320,320);
//	WindowHandle = glutCreateWindow("FlackEngine V0.02");
//
//	
//	// register callbacks
//	glutDisplayFunc(Render);
//	glutReshapeFunc(Resize);
//	glutIdleFunc(Render);
//	glutKeyboardFunc(NKeys);
//	glutSpecialFunc(SKeys);
//
//	glutMouseFunc(MButton);
//	glutMotionFunc(MMove);
//
//	// OpenGL init
//	glEnable(GL_DEPTH_TEST);
//	FLog("OpenGL Version: "+(string)((char*)glGetString(GL_VERSION)),true);
//	glewInit();
//
//	SimpleLoad();
//
//	glutMainLoop();
//	
//}
//
//
//void SimpleLoad()
//{
//	//glEnable(GL_LIGHTING);
//	//glLightModelfv(GL_LIGHT_MODEL_AMBIENT,ambientLight);
//
//	//glEnable(GL_COLOR_MATERIAL);
//
//
//	//glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE);
//
//	//glEnable(GL_FOG); // Turn Fog on
//	//glFogfv(GL_FOG_COLOR, 0.0f); // Set fog color to match background
//	//glFogf(GL_FOG_START, 5.0f); // How far away does the fog start
//	//glFogf(GL_FOG_END, 80.0f); // How far away does the fog stop
//	//glFogi(GL_FOG_MODE, GL_LINEAR); // Which fog equation to use
//
//
//	//glEnable( GL_TEXTURE_2D );
//	//Flak_T.dae
//
//	B_ComplianceTest();
//
//	Model = Loader.Read((char*) FPath.Dir_Add_Aliased("Models","Flak_T.dae").c_str());
//
//
//	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
//	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
//	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
//	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
//
//	//RManager.Texture_Get(FPath.Dir_Add_Aliased("Materials","pic.jpg"));
//}
//
//void SimpleRender()
//{
//
//
//  glColor3f(1.0f,1.0f,1.0f);            
//    glBegin(GL_QUADS);                  
//        glVertex3f(-1.0f, 3.0f, 0.0f);          
//        glVertex3f( 1.0f, 3.0f, 0.0f);          
//        glVertex3f( 1.0f,2.0f, 0.0f);          
//        glVertex3f(-1.0f,2.0f, 0.0f);         
//    glEnd();                       
//
//
//
//	glColor3f(0.5f,0.5f,1.0f); 
//
//	Model->Render();
//
//
//	//glPushMatrix();
//	//glMultTransposeMatrixf(Dat.mMatrix);
//
//
//	//glBegin(GL_TRIANGLES);
//	//for(int i=0;i<Dat.msize;i++)
//	//{
//	//	glTexCoord2f(DatT.mData[i*2+0], DatT.mData[i*2+1]);
//	//	glVertex3f(Dat.mData[i*3+0], Dat.mData[i*3+1], Dat.mData[i*3+2]);
//	//	glNormal3f(DatN.mData[i*3+0], DatN.mData[i*3+1], DatN.mData[i*3+2]);
//	//}
//	//glEnd();
//
//	//glPopMatrix();
//	
//
//}
