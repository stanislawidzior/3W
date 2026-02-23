import pygame
import math
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

class Scene:
    entities: list[Entity] = []

    def add_entity(self, entity : Entity):
        self.entities.append(entity)   

    def draw(self):
        for e in self.entities:
            e.draw()

    def translate(self, translation : pygame.Vector3):
        for e in self.entities:
            for ver in e.vertices:
                if translation.x != 0:
                    ver.x = ver.x + translation.x
                if translation.y != 0:
                    ver.y = ver.y + translation.y
                if translation.z != 0:
                    ver.z = ver.z + translation.z

    def rotate_y(self, angle):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))
        for e in self.entities:
            for ver in e.vertices:
                old_ver = ver
                ver.x = old_ver.x*cos + old_ver.z * sin
                ver.z = old_ver.z*cos - old_ver.x * sin


class Cube(Entity):
    indices = [
        [0,1,2,3],
        [4,5,6,7],
        [0,4,5,1],
        [2,6,7,3]
        ]
    vertices = []
    size = 0
    def __init__(self, size, position, rotation = 0):
        absolute_size = size
        absolute_size_half = size/2
        self.vertices = [
            pygame.Vector3(-absolute_size_half,-absolute_size_half,1),
            pygame.Vector3(-absolute_size_half,absolute_size_half,1),
            pygame.Vector3(absolute_size_half,absolute_size_half,1),
            pygame.Vector3(absolute_size_half,-absolute_size_half,1),
        
            pygame.Vector3(-absolute_size_half,-absolute_size_half, absolute_size + 1),
            pygame.Vector3(-absolute_size_half,absolute_size_half, absolute_size + 1),
            pygame.Vector3(absolute_size_half,absolute_size_half, absolute_size + 1),
            pygame.Vector3(absolute_size_half,-absolute_size_half, absolute_size + 1),
            ]
        for v in self.vertices:
            v.x += position.x
            v.y += position.y
    
    def draw(self):
        self.draw_vertices()
        self.draw_faces()
    def draw_vertices(self):    
        for v in self.vertices:
            if v.z < 0:
                print(v.z)
                continue
            projected = project_to_2d(v)
            pygame.draw.circle(screen, "red", translate(projected), 2)
    def is_visible(self,projected_vector):
        return projected_vector.x < screen.get_width() and projected_vector.x > 0 and projected_vector.y < screen.get_height() and projected_vector.y > 0 
    
    def draw_faces(self):
        for face in self.indices: 
            for i in range(len(face)):
                if self.is_visible(translate(project_to_2d(self.vertices[face[i]]))) :
                    pygame.draw.line(screen,"red", translate(project_to_2d(self.vertices[face[i]])), translate(project_to_2d(self.vertices[(face[(i +1)%len(face)])])))

def project_to_2d(vector3):
    return pygame.Vector2(
        vector3.x/vector3.z,
        vector3.y/vector3.z)

def translate(vector2):
    return pygame.Vector2(
        ((vector2.x + 1)/2)*screen.get_width(),
        (1 - (vector2.y + 1)/2)*screen.get_height())

cube_1 = Cube(0.2, pygame.Vector2(0,0))
scene = Scene()
scene.add_entity(cube_1)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    scene.draw()
    prev_mouse = mouse.get_rel()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        scene.translate(pygame.Vector3(0, 0, -0.2))
    if keys[pygame.K_s]:
        scene.translate(pygame.Vector3(0, 0, 0.2))
    if keys[pygame.K_a]:
        scene.translate(pygame.Vector3(0.2, 0, 0))
    if keys[pygame.K_d]:
        scene.translate(pygame.Vector3(-0.2, 0, 0))
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