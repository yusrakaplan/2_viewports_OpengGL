
""" Objelerin okunması çizilmesi ve texturelanması ayrı bir dosya
 olan objects.py dosyasında kodlanmıştır daha sonra buraya import edilmistir"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import objects
from pygame.locals import *

""" Orjine (0,0,0) yerleştirilmiş cube.obj dosyasından okunmuş 3B bir
nesneyi konumlandırıldı. """

class Cube(object):

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.rubik_id = objects.load_texture("rubik.png")
        self.cube = objects.ObjLoader("cube.obj")


    def render_scene(self):

        glClearColor(0.7, 0.9, 1, 1)
        self.cube.render_texture(self.rubik_id, ((0, 0), (1, 0), (1, 1), (0, 1)))

"""Kamerayı temsil eden yine cube.obj dosyasından okunan fakat camera.py ile texturalan
camera nesnesi ekrana çizdirilir."""

class Camera(object):
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.cam_id = objects.load_texture("camera.png")
        self.camera = objects.ObjLoader("cube.obj")

    def render_scene(self):
        glClearColor(0.7, 0.9, 1, 1)
        glScalef(0.2, 0.2, 0.2)
        self.camera.render_texture(self.cam_id, ((0, 0), (1, 0), (1, 1), (0, 1)))


def main():
    pygame.init()
    pygame.display.set_mode((1280, 480), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("PyOpengl Büt Ödevi")
    clock = pygame.time.Clock()


    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, 640, 480)
    gluPerspective(45, 640.0 / 480.0, 0.1, 200.0)

    cube = Cube()
    camera=Camera()
    camera_pos = [2.0, 0.0, -2.0]

    """Klavye tuşları ile kamera hareketleri tanımlanır ."""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            camera_pos[1] += 0.1
        if keys[K_DOWN]:
            camera_pos[1] -= 0.1
        if keys[K_LEFT]:
            camera_pos[0] -= 0.1
        if keys[K_RIGHT]:
            camera_pos[0] += 0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)

        """Sol viewportta ekranda hem kamerayı hem de orjindeki küp nesnesini 
        görüyoruz küp sabit kalmaktadır kamera haeket etmektedir."""

        # Left viewport
        glViewport(0, 0, 640, 480)
        glPushMatrix()
        glTranslatef(0, 0, -5.0)
        cube.render_scene()
        glTranslatef(*camera_pos)
        camera.render_scene()
        glPopMatrix()

        """Tanımladığımız kameranın bakış açısına göre nesneyi ekrana çizdirecek."""

        # Right viewport
        glViewport(640, 0, 640, 480)
        glPushMatrix()
        gluLookAt(*camera_pos,  # Eye position (camera position)
                  0.0, 0.0, 0.0,  # Center position (looking at the cube)
                  0.0, 1.0, 0.0)  # Up vector (camera's "up" direction)
        cube.render_scene()
        glPopMatrix()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()