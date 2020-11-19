import pygame
import random
import math

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# -- global constants
maxsizex = 25
maxsizey = 25
tilesize = 20
UIsectionsize = 5
enemymoverate = 7


# -- Blank Screen
size = (maxsizex * tilesize,maxsizey*tilesize + UIsectionsize * tilesize)
screen = pygame.display.set_mode(size)

# -- sprite calls
outerwallimg = pygame.transform.scale(pygame.image.load("outerwall.png").convert(), (tilesize,tilesize))
innerwallimg = pygame.transform.scale(pygame.image.load("innerwall.png").convert(), (tilesize,tilesize))
floorimg = pygame.transform.scale(pygame.image.load("floor.png").convert(), (tilesize,tilesize))
enemyimg = pygame.transform.scale(pygame.image.load("enemyting.png"), (tilesize,tilesize))
keyimg = pygame.transform.scale(pygame.image.load("key.png"), (tilesize//2,tilesize//2))
playerimg = pygame.transform.scale(pygame.image.load("player.png"), (tilesize,tilesize))

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

matrix = [[0 for x in range(maxsizey)] for y in range(maxsizex)]
for y in range(maxsizey):
            for x in range (maxsizex):
                if map[y][x] == " ":
                    matrix[y][x] = 1  
                elif map[y][x] == "#" or map[x][y] == "%":
                    matrix[y][x] = 0
                elif map[y][x] == "e": 
                    matrix[y][x] = 1
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
        self.image = outerwallimg
        #self.image.fill(color)
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
        self.image = innerwallimg
        self.rect = self.image.get_rect()
        # Set the position of the wall's attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        
class background(pygame.sprite.Sprite):
    # Define the constructor for the wall
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width*tilesize,height*tilesize])
        self.image = floorimg
        self.rect = self.image.get_rect()
        # Set the position of the wall's attributes
        self.rect.x = x_ref
        self.rect.y = y_ref

class key(pygame.sprite.Sprite):
    def __init__ (self,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([tilesize // 2,tilesize // 2])
        self.image = keyimg
        self.rect = self.image.get_rect()
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
        ##pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        self.image = playerimg
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.health = 100
        self.attack = 40
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
        self.image = pygame.Surface([width*tilesize,height*tilesize],pygame.SRCALPHA)
        self.image = enemyimg
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.health = 60
        self.attack = 20
        self.targetx = self.rect.x + self.width // 2
        self.targety = self.rect.y + self.height // 2
        self.movecounter = 0
    def update(self):
        #definitions for later calculations
        centrex = self.rect.x + (self.width * tilesize) // 2
        centrey = self.rect.y + (self.height * tilesize) // 2
        
        if self.health <= 0:
            new_key = key(centrex,centrey)
            all_sprites_list.add(new_key)
            key_list.add(new_key)
            PC.score += 30 + random.randrange(0,30)
            self.kill()
            
        
        xgrid = (centrex) // tilesize  
        ygrid = (centrey) // tilesize

        #pathfinding logic
        if (self.targetx == xgrid * tilesize) and (self.targety == ygrid * tilesize):
            start = grid.node(ygrid , xgrid )
            end = grid.node((PC.rect.y) //  tilesize, (PC.rect.x) // tilesize)
            path, runs = finder.find_path(start, end, grid)
            grid.cleanup()
            if len(path) <= 1:
                oneblock = True
            else:
                oneblock = False
                #print('operations:', runs, 'path length:', len(path))
                #print(grid.grid_str(path=path, start=start, end=end))
                self.targetx = (int(path[1][1]) * tilesize )
                self.targety = (int(path[1][0]) * tilesize )
        else:
            if (self.movecounter >= enemymoverate):
                self.movecounter = 0
                xdir = 0
                ydir = 0
                if self.rect.x < self.targetx:
                    xdir = 1
                elif self.rect.x > self.targetx:
                    xdir = -1
                elif self.rect.y < self.targety:
                    ydir = 1
                elif self.rect.y > self.targety:
                    ydir = -1
                self.rect.x += xdir * tilesize  // 1
                self.rect.y += ydir * tilesize // 1
                
            else:
                self.movecounter += 1

# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
key_list = pygame.sprite.Group()
back_sprites_list = pygame.sprite.Group()
        

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

## --== instantiates the map
for y in range(maxsizey):
    for x in range (maxsizex):
        if (map[y][x] == " ") or (map[y][x] == "e"):
            new_wall = background(RED, 1, 1, x*tilesize, y *tilesize)
            back_sprites_list.add(new_wall)
        if map[y][x] == "%":
            new_wall = outerwall((200,30,30), 1, 1, x*tilesize, y *tilesize)
            wall_list.add(new_wall)
            all_sprites_list.add(new_wall)
        elif map[y][x] == "#":
            new_wall = innerwall(RED, 1, 1, x*tilesize, y *tilesize)
            wall_list.add(new_wall)
            all_sprites_list.add(new_wall)
        elif map[y][x] == "e":
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

    player_collide_list = pygame.sprite.spritecollide(PC, enemy_list, False)
    for foo in player_collide_list:
        PC.health -= random.randrange(0,foo.attack)
        foo.health -= random.randrange(0,PC.attack)

    

    player_collide_list = pygame.sprite.spritecollide(PC, key_list, True)
    for foo in player_collide_list:
        PC.money += 1

    # -- screen background is WHITE

    screen.fill(WHITE)

    # -- Draw here
    back_sprites_list.draw(screen)
    all_sprites_list.draw(screen)
    all_sprites_list.update()
    text = font.render(" | HP: " + str(PC.health) \
                           + " | Keys: " + str(PC.money) + " | Score: " \
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
