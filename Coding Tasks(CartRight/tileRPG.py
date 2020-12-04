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
enemymoverate = 1
enemyspeed = 2
Pviewrange  = 3
EVlength = 4
EVwidth = 1
global caught


# -- Blank Screen
size = (maxsizex * tilesize,maxsizey*tilesize + UIsectionsize * tilesize)
screen = pygame.display.set_mode(size)

# -- sprite calls
menu = pygame.transform.scale(pygame.image.load("Mainmenu.png").convert(),(maxsizex * tilesize, (maxsizey + UIsectionsize) * tilesize))  
outerwallimg = pygame.transform.scale(pygame.image.load("outerwall.png").convert(), (tilesize,tilesize))
innerwallimg = pygame.transform.scale(pygame.image.load("innerwall.png").convert(), (tilesize,tilesize))
floorimg = pygame.transform.scale(pygame.image.load("floor.png").convert(), (tilesize,tilesize))
enemyimg = (pygame.transform.scale(pygame.image.load("rommbadrone1.png"), (tilesize,tilesize)),pygame.transform.scale(pygame.image.load("rommbadrone2.png"), (tilesize,tilesize)),pygame.transform.scale(pygame.image.load("rommbadrone3.png"), (tilesize,tilesize)),pygame.transform.scale(pygame.image.load("rommbadrone4.png"), (tilesize,tilesize)))
keyimg = pygame.transform.scale(pygame.image.load("bag.png"), (tilesize,tilesize))
stairsimg = pygame.transform.scale(pygame.image.load("stairs.png"), (tilesize,tilesize))
playerimg = pygame.transform.scale(pygame.image.load("player.png"), (tilesize,tilesize))
portalimg = pygame.transform.scale(pygame.image.load("hole.png"), (tilesize * 2,tilesize * 2))
poverlay = pygame.transform.scale(pygame.image.load("poverlay.png"), (tilesize * Pviewrange * 2, tilesize * Pviewrange * 2))
doverlay = pygame.transform.scale(pygame.image.load("doverlay.png"), (tilesize * maxsizex, tilesize * maxsizey))

map = [\
    "%%%%%%%%%%%%%%%%%%%%%%%%%",
    "%                      e%",
    "%                       %",
    "%  ###  ###   ###  ###  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #      ## ##      #  %",
    "%  #      #   #      #  %",
    "%  #                 #  %",
    "%  #      #   #      #  %",
    "%  #      ## ##      #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  #                 #  %",
    "%  #                 #  %",
    "%  #      #   #      #  %",
    "%  #      #   #      #  %",
    "%  ###  ###   ###  ###  %",
    "%                       %",
    "%e                      %",
    "%%%%%%%%%%%%%%%%%%%%%%%%%"]

matrix = [[0 for x in range(maxsizey)] for y in range(maxsizex)]
for y in range(maxsizey):
            for x in range (maxsizex):
                #if map[y][x] == " ":
                #    matrix[y][x] = 1  
                if map[y][x] == "#" or map[x][y] == "%": 
                    matrix[y][x] = 0
                elif map[y][x] == "e": 
                    matrix[y][x] = 1
                else:
                    matrix[y][x] = random.randint(1,4)
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
        self.image = pygame.Surface([tilesize,tilesize])
        self.image = keyimg
        self.rect = self.image.get_rect()
        self.rect.x = x_ref
        self.rect.y = y_ref



class stairs(pygame.sprite.Sprite):
    def __init__ (self,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([tilesize,tilesize])
        self.image = stairsimg
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
        self.dirx = 0
        self.diry = 0
    def update(self):
        updated = True

class overlay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([tilesize*maxsizex,tilesize*maxsizey],pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0,150))
        pygame.draw.circle(self.image, (0,0,0,0), (PC.rect.center),tilesize*Pviewrange)
    def update(self):        
        self.image.fill((0,0,0,200))
        pygame.draw.circle(self.image, (0,0,0,0), (PC.rect.center),tilesize*Pviewrange)

class enemy(pygame.sprite.Sprite):
    # Define the constructor for the player
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width*tilesize,height*tilesize],pygame.SRCALPHA)
        self.image = enemyimg[0]
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        #pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.health = 60
        self.attack = 20
        self.targetx = self.rect.x + tilesize // 2
        self.targety = self.rect.y + tilesize // 2
        self.movecounter = 0
    def update(self):
        #definitions for later calculations
        centrex = self.rect.x + (self.width * tilesize) // 2
        centrey = self.rect.y + (self.height * tilesize) // 2
        
        if self.health <= 0:
            self.kill()
            
        
        xgrid = (centrex) // tilesize  
        ygrid = (centrey) // tilesize

        #pathfinding logic
        if (self.targetx == self.rect.center[0] ) and (self.targety == self.rect.center[1]):
            grid.cleanup()
            start = grid.node(ygrid , xgrid )
            end = grid.node((PC.rect.x) //  tilesize, (PC.rect.y) // tilesize)
            path, runs = finder.find_path(start, end, grid)
            if len(path) <= 1:
                oneblock = True
            else:
                oneblock = False
                #print('operations:', runs, 'path length:', len(path))
                #print(grid.grid_str(path=path, start=start, end=end))
                self.targetx = (int(path[1][1]) * tilesize + tilesize // 2)
                self.targety = (int(path[1][0]) * tilesize + tilesize // 2 )
        else:
            global Caught
            if (self.movecounter >= enemymoverate):
                self.movecounter = 0
                xdir = 0
                ydir = 0                
                if self.rect.center[0] < self.targetx:
                    xdir = 1
                    self.image = enemyimg[1]
                    pygame.draw.polygon(screen, (255,255,10,175), (self.rect.center,(self.rect.center[0] + tilesize * EVlength,self.rect.center[1] + tilesize * EVwidth),(self.rect.center[0] + tilesize * EVlength,self.rect.center[1] - tilesize * EVwidth)))
                    if (abs(PC.rect.center[0] - self.rect.center[0]) <= tilesize * EVlength):
                        if (abs(PC.rect.center[1] - self.rect.center[1]) <= (EVwidth / EVlength) *  abs(PC.rect.center[0] - self.rect.center[0])):
                            Caught = True
                elif self.rect.center[0] > self.targetx:
                    xdir = -1
                    self.image = enemyimg[3]
                    pygame.draw.polygon(screen, (255,255,10,175), (self.rect.center,(self.rect.center[0] - tilesize * EVlength,self.rect.center[1] + tilesize * EVwidth),(self.rect.center[0] - tilesize * EVlength,self.rect.center[1] - tilesize * EVwidth)))
                    if (abs(PC.rect.center[0] - self.rect.center[0]) <= tilesize * EVlength):
                        if (abs(PC.rect.center[1] - self.rect.center[1]) <= (EVwidth / EVlength) *  abs(PC.rect.center[0] - self.rect.center[0])):
                            Caught = True
                elif self.rect.center[1] < self.targety:
                    ydir = 1#
                    self.image = enemyimg[2]
                    pygame.draw.polygon(screen, (255,255,10,175), (self.rect.center,(self.rect.center[0] + tilesize * EVwidth,self.rect.center[1] + tilesize * EVlength),(self.rect.center[0] - tilesize * EVwidth,self.rect.center[1] + tilesize * EVlength)))
                    if (abs(PC.rect.center[1] - self.rect.center[1]) <= tilesize * EVlength):
                        if (abs(PC.rect.center[0] - self.rect.center[0]) <= (EVwidth / EVlength) *  abs(PC.rect.center[1] - self.rect.center[1])):
                            Caught = True
                elif self.rect.center[1] > self.targety:
                    ydir = -1
                    self.image = enemyimg[0]
                    pygame.draw.polygon(screen, (255,255,10,175), (self.rect.center,(self.rect.center[0] - tilesize * EVwidth,self.rect.center[1] - tilesize * EVlength),(self.rect.center[0] + tilesize * EVwidth,self.rect.center[1] - tilesize * EVlength)))
                    if (abs(PC.rect.center[1] - self.rect.center[1]) <= tilesize * EVlength):
                        if (abs(PC.rect.center[0] - self.rect.center[0]) <= (EVwidth / EVlength) *  abs(PC.rect.center[1] - self.rect.center[1])):
                             Caught = True
                #self.rect.x += xdir * tilesize  // 1
                #self.rect.y += ydir * tilesize // 1
                self.rect.x += xdir * enemyspeed
                self.rect.y += ydir * enemyspeed
            else:
                self.movecounter += 1

# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
key_list = pygame.sprite.Group()
platforms = list()
player_list = pygame.sprite.Group()
back_sprites_list = pygame.sprite.Group()
DOlist = pygame.sprite.Group()
        

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf',32)
### -- Game Loop
Caught = False
ingame = False

while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ingame = True
                    level = 1
    screen.blit(menu,(0,0))
    if ingame == True:
        Caught = False 
        for foo in all_sprites_list:
            foo.kill() 
        for foo in wall_list:
            foo.kill() 
        for foo in enemy_list:
            foo.kill() 
        for foo in key_list:
            foo.kill() 
        for foo in player_list:
            foo.kill()
        for foo in DOlist:
            foo.kill()
        newstairs = stairs((maxsizex // 2) * tilesize,(maxsizey // 2) * tilesize)
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
                    platforms.append(new_wall)
                elif map[y][x] == "#":
                    new_wall = innerwall(RED, 1, 1, x*tilesize, y *tilesize)
                    wall_list.add(new_wall)
                    all_sprites_list.add(new_wall)
                    platforms.append(new_wall)
                elif map[y][x] == "e":
                    new_enemy = enemy(GREEN, 1, 1, x*tilesize, y *tilesize)
                    enemy_list.add(new_enemy)
                    all_sprites_list.add(new_enemy)        

        # -- instantiates player
        PC = player(BLUE,tilesize ,tilesize ,tilesize*(maxsizex//2),tilesize*(maxsizey//2))
        #all_sprites_list.add(PC)
        player_list.add(PC)
        
        no = 0
        while no < level + 2:
            puckspawned = False
            while not puckspawned:
                xpos = random.randrange(0,maxsizex)
                ypos = random.randrange(0,maxsizey)
                if map[ypos][xpos] == " ":
                    puckspawned = True
                    new_key = key(xpos * tilesize,ypos * tilesize)
                    all_sprites_list.add(new_key)
                    key_list.add(new_key)
                    #PC.score += 30 + random.randrange(0,30)
            no += 1

        DO = overlay()
        DOlist.add(DO)
        while Caught == False:
            PC_oldX = PC.rect.x
            PC_oldY = PC.rect.y
            # -- user input and controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        PC.dirx = 0            
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        PC.dirx = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                PC.rect.x -= tilesize // 4
                PC.dirx = -1
            elif keys[pygame.K_RIGHT]:
                PC.rect.x += tilesize // 4
                PC.dirx = 1


            # -- Game Logic goes after this comment
            player_collide_list = pygame.sprite.spritecollide(PC, wall_list, False)
            for foo in player_collide_list:
                if (pygame.Rect(PC.rect.x + int(tilesize * 0.25) + 1,PC.rect.y,  # +1
                                    PC.rect.width, PC.rect.height)
                        .colliderect(foo.rect) and PC.rect.x + int(tilesize * 0.25) // 2 <= foo.rect.x and PC.dirx == 1):
                    PC.rect.right = foo.rect.left
                elif (pygame.Rect(PC.rect.x + (int(tilesize * 0.25) - 1),PC.rect.y,  # +1
                                    PC.rect.width, PC.rect.height)
                        .colliderect(foo.rect) and PC.rect.x + int(tilesize * 0.25) // 2 >= foo.rect.x and PC.dirx == -1):
                    PC.rect.left = foo.rect.right

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                PC.rect.y -= tilesize // 4
                PC.diry = 1
            elif keys[pygame.K_DOWN]:
                PC.rect.y += tilesize // 4
                PC.diry = -1

            
            player_collide_list = pygame.sprite.spritecollide(PC, wall_list, False)
                
            for foo in player_collide_list:
                if (pygame.Rect(PC.rect.x, PC.rect.y + (int(tilesize * 0.25) - 1), # +1
                                    PC.rect.width, PC.rect.height)
                        .colliderect(foo.rect) and PC.rect.y + int(tilesize * 0.25) // 2 >= foo.rect.y and PC.diry == 1):
                    PC.rect.top = foo.rect.bottom
                elif (pygame.Rect(PC.rect.x, PC.rect.y + int(tilesize // 4) + 1, # +1
                                    PC.rect.width, PC.rect.height)
                        .colliderect(foo.rect) and PC.rect.y + int(tilesize * 0.25) // 2 <= foo.rect.y and PC.diry == -1):
                    PC.rect.bottom = foo.rect.top

            player_collide_list = pygame.sprite.spritecollide(PC, enemy_list, False)
            for foo in player_collide_list:
                PC.health -= random.randrange(0,foo.attack)
                foo.health -= random.randrange(0,PC.attack)
            
            if (2 + level - PC.money) == 0 and picked == True:
                newstairs.kill()
                newstairs = stairs((maxsizex // 2) * tilesize,(maxsizey // 2) * tilesize)
                all_sprites_list.add(newstairs)
                key_list.add(newstairs)
                picked == False
                #PC.money = 0
                #PC.score += 2 * level
                #level += 1

            

            player_collide_list = pygame.sprite.spritecollide(PC, key_list, True)
            for foo in player_collide_list:
                if (2 + level - PC.money) == 0:                    
                    for foo2 in enemy_list:
                        foo2.kill()
                    PC.rect.x = (maxsizex // 2) * tilesize
                    PC.rect.y = (maxsizey // 2) * tilesize
                    PC.money = 0
                    print("iteration" + str(level))
                    level += 1
                    
                    for y in range(maxsizey):
                        for x in range (maxsizex):
                            if map[y][x] == "e":
                                new_enemy = enemy(GREEN, 1, 1, x*tilesize, y *tilesize)
                                enemy_list.add(new_enemy)
                                all_sprites_list.add(new_enemy)

                    
                    no = 0
                    while no < level + 2:
                        puckspawned = False
                        while not puckspawned:
                            xpos = random.randrange(0,maxsizex)
                            ypos = random.randrange(0,maxsizey)
                            if map[ypos][xpos] == " ":
                                puckspawned = True
                                new_key = key(xpos * tilesize,ypos * tilesize)
                                all_sprites_list.add(new_key)
                                key_list.add(new_key)
                                #PC.score += 30 + random.randrange(0,30)
                        no += 1
                    foo.kill()
                else:
                    PC.money += 1
                    PC.score += level
                    foo.kill()
                    picked = True

            # -- screen background is WHITE

            screen.fill(WHITE)

            # -- Draw here
            back_sprites_list.draw(screen)
            all_sprites_list.draw(screen)
            all_sprites_list.update()
            player_list.draw(screen)
            player_list.update()
            text = font.render(" | Level: " + str(level) \
                                   + " | Bags Left: " + str(2 + level - PC.money) + " | Score: " \
                               + str(PC.score) + " | ", True, BLACK)
            textRect = text.get_rect()
            textRect.center = ((maxsizex * tilesize) // 2,\
                               maxsizey*tilesize + (UIsectionsize * tilesize) // 2)
            screen.blit(text,textRect)

            DOlist.draw(screen)
            DOlist.update()

            # -- flip display to reveal new position of objects
            pygame.display.flip()

            # - the clock ticks over
            clock.tick(60)
        ingame = False
        # - end of game loop
    

    text = font.render("press space to start", True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((maxsizex * tilesize) // 2,\
                       maxsizey*tilesize + (UIsectionsize * tilesize) // 2)
    screen.blit(text,textRect)
    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)
pygame.quit()
