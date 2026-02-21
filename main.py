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

class Cube:
    cube_indices = []
    cube_vertices = []
    size = 0
    def __init__(self, size, position, rotation = 0):
        absolute_size = screen.get_width() / size
        absolute_size_half = absolute_size/2
        self.cube_vertices = [
            pygame.Vector3(-absolute_size_half,-absolute_size_half,1),
            pygame.Vector3(-absolute_size_half,absolute_size_half,1),
            pygame.Vector3(absolute_size_half,absolute_size_half,1),
            pygame.Vector3(absolute_size_half,-absolute_size_half,1),
        
            pygame.Vector3(-absolute_size_half,-absolute_size/2, absolute_size + 1),
            pygame.Vector3(-absolute_size_half,absolute_size/2, absolute_size + 1),
            pygame.Vector3(absolute_size_half,absolute_size/2, absolute_size + 1),
            pygame.Vector3(absolute_size_half,-absolute_size/2, absolute_size + 1),
            ]
        absolute_position_x = (screen.get_width()/2 - position.x )/screen.get_width()
        absolute_position_y = (screen.get_height()/2 - position.y )/screen.get_height()
        for v in self.cube_vertices:
            v.x += absolute_position_x
            v.y += absolute_position_y
            


cube_edge_width = 10
cube_vertices = [
    pygame.Vector3(-0.5,-0.5,1),
    pygame.Vector3(-0.5,0.5,1),
    pygame.Vector3(0.5,0.5,1),
    pygame.Vector3(0.5,-0.5,1),
    
    pygame.Vector3(-0.5,-0.5,2),
    pygame.Vector3(-0.5,0.5,2),
    pygame.Vector3(0.5,0.5,2),
    pygame.Vector3(0.5,-0.5,2),
    
]
cube_indices = [
    [0,1,2,3],
    [4,5,6,7],
    [0,4,5,1],
    [2,6,7,3]
]

cube_1 = Cube(50, pygame.Vector2(200,200))
def draw_cubes(cube_vertices):
    counter = 0
    for v in cube_vertices:
        counter += 1
        projected = project_to_2d(v)
        pygame.draw.circle(screen, "red", translate(projected), 2)
        
        ##pygame.draw.line(screen, "red", translate_to_screen_coord(projected), translate_to_screen_coord(project_to_2d(cube_vertices[counter%len(cube_vertices)]) ), 1)
        ##pygame.draw.line(screen, "red", translate_to_screen_coord(projected), translate_to_screen_coord(project_to_2d(cube_vertices[(counter+2)%len(cube_vertices)]) ), 1)
       
        #projected = project_to_2d(pygame.Vector3(v.x +1, v.y, v.z))
        #pygame.draw.circle(screen, "red", translate_to_screen_coord(projected), 2)
        ##pygame.draw.line(screen, "red", translate_to_screen_coord(projected), translate_to_screen_coord(project_to_2d(cube_vertices[counter%len(cube_vertices)]) ), 1)
        ##pygame.draw.line(screen, "red", translate_to_screen_coord(projected), translate_to_screen_coord(project_to_2d(cube_vertices[(counter+2)%len(cube_vertices)]) ), 1)
    draw_faces()

def draw_faces():
    for face in cube_indices:
        for i in range(len(face)):
            pygame.draw.line(screen,"red", translate(project_to_2d(cube_vertices[face[i]])), translate(project_to_2d(cube_vertices[(face[(i +1)%len(face)])])))


        

def project_to_2d(vector3):
    return pygame.Vector2(
        vector3.x/vector3.z,
        vector3.y/vector3.z)

def translate(vector2):
    return pygame.Vector2(
        ((vector2.x + 1)/2)*screen.get_width(),
        (1 - (vector2.y + 1)/2)*screen.get_height())

def rotate_y(vector3, angle):
    cos = math.cos(math.radians(angle))
    sin = math.sin(math.radians(angle))
    return pygame.Vector3(
        vector3.x*cos + vector3.z * sin,
        vector3.y,
        vector3.z*cos - vector3.x * sin
    )

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    draw_cubes(cube_vertices)
    prev_mouse = mouse.get_rel()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        for i in range(len(cube_vertices)):
            cube_vertices[i].z = cube_vertices[i].z - 0.02
    if keys[pygame.K_s]:
       for i in range(len(cube_vertices)):
            cube_vertices[i].z = cube_vertices[i].z + 0.02
    if keys[pygame.K_a]:
        for i in range(len(cube_vertices)):
            cube_vertices[i].x = cube_vertices[i].x + 0.02
    if keys[pygame.K_d]:
        for i in range(len(cube_vertices)):
            cube_vertices[i].x = cube_vertices[i].x - 0.02
    if prev_mouse[0] != 0:
        for i in range(len(cube_vertices)):
            cube_vertices[i] = rotate_y(cube_vertices[i], prev_mouse[0]/10 * -1)
    mouse.set_pos([screen.get_width()/2,screen.get_height()/2])
    mouse.get_rel()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(30) / 1000

pygame.quit()