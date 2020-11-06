import pygame

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# -- global constants
maxsizex = 25
maxsizey = 25
tilesize = 20
UIsectionsize = 5
enemymoverate = 60

map = [\
    "%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%       #              e%",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%       #               %",
    "%        #              %",
    "%         #             %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%                       %",
    "%e                     e%",
    "%%%%%%%%%%%%%%%%%%%%%%%%%"]

matrix = [[0 for y in range(maxsizey)] for x in range(maxsizex)]
for y in range(maxsizey):
            for x in range (maxsizex):
                if map[x][y] == " ":
                    matrix[x][y] = 1  
                elif map[x][y] == "#" or map[x][y] == "%":
                    matrix[x][y] = 0
                elif map[x][y] == "e": 
                    matrix[x][y] = 1
grid = Grid(matrix=matrix)
finder = AStarFinder(diagonal_movement=DiagonalMovement.never)

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE =(0,0,255)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (maxsizex * tilesize,maxsizey*tilesize + UIsectionsize * tilesize)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("TileRPG")

#class definitions

## -- wall class
class outerwall(pygame.sprite.Sprite):
    # Define the constructor for the wall
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width*tilesize,height*tilesize])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Set the position of the wall's attributes
        self.rect.x = x_ref
        self.rect.y = y_ref

class innerwall(pygame.sprite.Sprite):
    # Define the constructor for the wall
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width*tilesize,height*tilesize])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Set the position of the wall's attributes
        self.rect.x = x_ref
        self.rect.y = y_ref

## -- the player class (sprite)
class player(pygame.sprite.Sprite):
    # Define the constructor for the player
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height],pygame.SRCALPHA)
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.health = 100
        self.money = 0
        self.score = 0
    def update(self):
        updated = True

class enemy(pygame.sprite.Sprite):
    # Define the constructor for the player
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width*tilesize,height*tilesize])
        self.image.fill(color)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.health = 60
        self.targetx = self.rect.x + self.width // 2
        self.targety = self.rect.y + self.height // 2
        self.movecounter = 0
    def update(self):
        #definitions for later calculations
        xgrid = (self.rect.x) // tilesize  
        ygrid = (self.rect.y) // tilesize
        centrex = self.rect.x + (self.width * tilesize) // 2
        centrey = self.rect.y + (self.height * tilesize) // 2

        #pathfinding logic
        if (self.targetx == centrex) and (self.targety == centrey):
            start = grid.node(ygrid - 1, xgrid - 1)
            end = grid.node((PC.rect.y + PC.rect.height // 2) //  tilesize, (PC.rect.x + PC.rect.width // 2) // tilesize)
            path, runs = finder.find_path(start, end, grid)
            grid.cleanup()
            if len(path) <= 1:
                oneblock = True
            else:
                oneblock = False
                self.targetx = (int(path[1][1]) * tilesize + tilesize // 2)
                self.targety = (int(path[1][0]) * tilesize + tilesize // 2)
        else:
            if (self.movecounter >= enemymoverate):
                self.movecounter = 0
                xdir = 0
                ydir = 0
                if centrex < self.targetx:
                    xdir = 1
                elif centrex > self.targetx:
                    xdir = -1
                elif centrey < self.targety:
                    ydir = 1
                elif centrey > self.targety:
                    ydir = -1
                self.rect.x += xdir * tilesize  // 2
                self.rect.y += ydir * tilesize // 2
                
            else:
                self.movecounter += 1

# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
        

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

## --== instantiates the map
for y in range(maxsizey):
    for x in range (maxsizex):
        if map[y][x] == "%":
            new_wall = outerwall((200,30,30), 1, 1, x*tilesize, y *tilesize)
            wall_list.add(new_wall)
            all_sprites_list.add(new_wall)
        if map[y][x] == "#":
            new_wall = innerwall(RED, 1, 1, x*tilesize, y *tilesize)
            wall_list.add(new_wall)
            all_sprites_list.add(new_wall)
        if map[y][x] == "e":
            new_enemy = enemy(GREEN, 1, 1, x*tilesize, y *tilesize)
            enemy_list.add(new_enemy)
            all_sprites_list.add(new_enemy)

# -- instantiates player
PC = player(BLUE,tilesize ,tilesize ,tilesize*(maxsizex//2),tilesize*(maxsizey//2))
all_sprites_list.add(PC)


font = pygame.font.Font('freesansbold.ttf',32)
### -- Game Loop

while not done:
    PC_oldX = PC.rect.x
    PC_oldY = PC.rect.y
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        PC.rect.x -= tilesize // 4
    elif keys[pygame.K_RIGHT]:
        PC.rect.x += tilesize // 4
    if keys[pygame.K_UP]:
        PC.rect.y -= tilesize // 4
    elif keys[pygame.K_DOWN]:
        PC.rect.y += tilesize // 4


    # -- Game Logic goes after this comment
    player_collide_list = pygame.sprite.spritecollide(PC, wall_list, False)
    for foo in player_collide_list:
        PC.rect.x = PC_oldX
        PC.rect.y = PC_oldY

    # -- screen background is WHITE

    screen.fill(WHITE)

    # -- Draw here
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    text = font.render(" | HP: " + str(PC.health) \
                           + " | Money: " + str(PC.money) + " | Score: " \
                       + str(PC.score) + " | ", True, BLACK)
    textRect = text.get_rect()
    textRect.center = ((maxsizex * tilesize) // 2,\
                       maxsizey*tilesize + (UIsectionsize * tilesize) // 2)
    screen.blit(text,textRect)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()