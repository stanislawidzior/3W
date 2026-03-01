import pygame
import math
import copy
# pygame setup

pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
mouse = pygame.mouse
mouse.set_visible(False)
running = True
dt = 0

class Entity:
    vertices = []
    def draw():
        pass
class Cube(Entity):
    indices = [
        [0,1,2,3],
        [4,5,6,7],
        [0,4,5,1],
        [2,6,7,3]
        ]
    y_rotation_sum = 0
    translation_sum = pygame.Vector3(0,0,0)
    vertices = []
    base = []
    size = 0
    def __init__(self, size, position, rotation = 0):
        absolute_size_half = size/2
        self.vertices = [
            pygame.Vector3(-absolute_size_half,-absolute_size_half,-absolute_size_half),
            pygame.Vector3(-absolute_size_half,absolute_size_half,-absolute_size_half),
            pygame.Vector3(absolute_size_half,absolute_size_half,-absolute_size_half),
            pygame.Vector3(absolute_size_half,-absolute_size_half,-absolute_size_half),
        
            pygame.Vector3(-absolute_size_half,-absolute_size_half, absolute_size_half),
            pygame.Vector3(-absolute_size_half,absolute_size_half, absolute_size_half),
            pygame.Vector3(absolute_size_half,absolute_size_half, absolute_size_half),
            pygame.Vector3(absolute_size_half,-absolute_size_half, absolute_size_half),
            ]
        self.translation_sum = position
        self.base = copy.deepcopy(self.vertices)
        self.translate(position)
   
    def rotate(self, angle):
        
        print(self.y_rotation_sum)
        for ver in self.vertices:
            ver.update(ver.rotate_y_rad(angle))
        
   

    def update(self, rotation = 0):

        self.vertices.clear()
        self.vertices = copy.deepcopy(self.base)
        self.translate(self.translation_sum)
        self.rotate(self.y_rotation_sum)

    def translate(self, translation):
        for v in self.vertices:
            v.x += translation.x
            v.y += translation.y
            v.z += translation.z

    def draw(self):
        self.update()
        self.draw_vertices()
        self.draw_faces()
    
    def draw_vertices(self):    
        for v in self.vertices:
            if v.z < 0:
                print(v.z)
                continue
            projected = project_to_2d(v)
            pygame.draw.circle(screen, "red", translate_to_coord(projected), 2)
    
    def is_visible(self,projected_vector):
        return projected_vector.x < screen.get_width() and projected_vector.x > 0 and projected_vector.y < screen.get_height() and projected_vector.y > 0 
    
    def draw_faces(self):
        for face in self.indices: 
            for i in range(len(face)):
                if self.is_visible(translate_to_coord(project_to_2d(self.vertices[face[i]]))) :
                    pygame.draw.line(screen,"red", translate_to_coord(project_to_2d(self.vertices[face[i]])), translate_to_coord(project_to_2d(self.vertices[(face[(i +1)%len(face)])])))

class Scene:
    entities: list[Cube] = []

    def add_entity(self, entity : Cube):
        self.entities.append(entity)   

    def draw(self):
        for e in self.entities:
            e.draw()

    def translate(self, translation : pygame.Vector3):
        for e in self.entities:
            e.translation_sum.update(e.translation_sum.x + translation.x, e.translation_sum.y + translation.y, e.translation_sum.z + translation.z )
            for ver in e.vertices:
                if translation.x != 0:
                    ver.x = ver.x + translation.x
                if translation.y != 0:
                    ver.y = ver.y + translation.y
                if translation.z != 0:
                    ver.z = ver.z + translation.z

    def rotate_y(self, angle):
        for e in self.entities:
            e.y_rotation_sum += math.radians(angle)
            e.rotate(e.y_rotation_sum)
        





def project_to_2d(vector3):
    return pygame.Vector2(
        vector3.x/vector3.z,
        vector3.y/vector3.z)

def translate_to_coord(vector2):
    return pygame.Vector2(
        ((vector2.x + 1)/2)*screen.get_width(),
        (1 - (vector2.y + 1)/2)*screen.get_height())


cube_1 = Cube(0.2, pygame.Vector3(0,0,1))
scene = Scene()
scene.add_entity(cube_1)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    scene.draw()
    prev_mouse = mouse.get_rel()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scene.translate(pygame.Vector3(0, 0, -0.1))
    if keys[pygame.K_s]:
        scene.translate(pygame.Vector3(0, 0, 0.1))
    if keys[pygame.K_a]:
        scene.translate(pygame.Vector3(0.1, 0, 0))
    if keys[pygame.K_d]:
        scene.translate(pygame.Vector3(-0.1, 0, 0))
    if keys[pygame.K_r]:
        cube_1.local_rotate(10)
    if prev_mouse[0] != 0:
        scene.rotate_y(prev_mouse[0]/10 * -1)
    
    mouse.set_pos([screen.get_width()/2,screen.get_height()/2])
    mouse.get_rel()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(30) / 1000

pygame.quit()