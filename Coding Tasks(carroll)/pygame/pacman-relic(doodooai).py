import pygame
import random
import math
from math import atan2, degrees, pi

# -- global constants
map =\
    [["#","#","#","#","_","_","#","#","#","#","#","#","#","#","_","_","#","#","#","#"],
    ["|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","|"],
    ["|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","|"],
    ["#","#"," ","#","#","#","#","#"," "," "," ","#"," ","#","#","#","#","#"," ","#"],
    ["#"," "," "," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"," ","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," ","#"],
    ["#"," ","#"," "," "," ","#"," "," "," "," "," ","#"," "," "," ","#"," "," ","#"],
    ["#"," ","#","#","#"," ","#"," "," "," "," "," ","#","#","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#"," ","#"," ","#","#"," "," "," "," ","#"," ","#"," ","#","#"," ","#"],
    ["|"," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," ","|"],
    ["|"," "," "," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," ","|"],
    ["#","#"," "," ","#"," ","#"," "," "," "," ","#"," "," ","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," ","#"],
    ["#"," ","#"," ","#"," "," "," "," "," "," "," ","#"," ","#"," "," "," "," ","#"],
    ["#"," ","#"," ","#"," ","#"," "," "," "," "," ","#"," ","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," ","#"],
    ["|"," "," ","#"," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," ","|"],
    ["|"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","|"],
    ["#","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," ","#"],
    ["#"," ","#"," "," "," ","#"," "," "," "," "," ","#"," "," "," ","#"," "," ","#"],
    ["#"," ","#","#","#"," ","#"," "," "," "," "," ","#","#","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"," "," "," "," "," ","#"," "," "," "," "," "," "," "," "," ","#"," "," ","#"],
    ["#"," ","#","#","#"," ","#","#"," "," "," "," ","#","#","#"," ","#","#"," ","#"],
    ["|"," "," "," ","#"," ","#"," ","e"," "," "," "," "," ","#"," ","#"," "," ","|"],
    ["|"," "," "," ","#"," ","#"," "," "," "," "," "," "," ","#"," ","#"," "," ","|"],
    ["#","#"," "," ","#"," ","#"," "," "," "," "," "," "," ","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","#"],
    ["#"," ","#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," ","#"],
    ["#"," ","#"," ","#"," "," "," "," "," "," "," ","#"," ","#"," "," "," "," ","#"],
    ["#"," ","#"," ","#"," ","#"," "," "," ","#"," ","#"," ","#"," ","#"," "," ","#"],
    ["#"," "," "," "," "," "," "," "," "," ","#"," "," "," "," "," "," "," "," ","#"],
    ["#","#","#","#","_","_","#","#","#","#","#","#","#","#","_","_","#","#","#","#"]]

maxsizex = 40
maxsizey = 20
#global control variants (to tweak + improve the game
playermovespeed = 2
enemymovespeed = 3
pointspawnfrequency = 30
startinglives = 1

# -- Colours
BLACK = (0,0,0)
DARKGRAY = (50,50,50)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (maxsizex * 20,maxsizey*20)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("PacMan")

# --- class definitions
## -- Define the class tile which is a sprite
class tile(pygame.sprite.Sprite):
    # Define the constructor for invader
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref

class pointpuck(pygame.sprite.Sprite):
    # Define the constructor for invader
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref

class player(pygame.sprite.Sprite):
    # Define the constructor for invader
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.speedx = 0
        self.speedy = 0
        self.score = 0
        self.lives = startinglives
    def update(self):
        self.rect.x += self.speedx*playermovespeed
        self.rect.y += self.speedy*playermovespeed
    def player_speed_update(self,xmult,ymult):
        self.speedx = xmult
        self.speedy = ymult

class enemy(pygame.sprite.Sprite):
    # Define the constructor for invader
    def __init__(self, color, width, height, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([width,height])
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, color, (width//2, height//2), width//2)
        # Set the position of the player attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.speedx = 0
        self.speedy = 0
        self.width = width
        self.height = height
    def update(self):
        dir = ""
        xgrid = (self.rect.x + self.width)// 20  
        ygrid = (self.rect.y + self.height) // 20 
        xdir = 0
        ydir = 0
        freebool = False
        if (pacman.rect.x > self.rect.x + self.width//2):
            xdir = 1
            dir += "R"
        elif (pacman.rect.x < self.rect.x + self.width // 2):
            xdir = -1
            dir += "L"
        if (pacman.rect.y > self.rect.y + self.height // 2):
            ydir = 1
            dir += "D"
        elif (pacman.rect.y < self.rect.y + self.height // 2):
            ydir = -1
            dir += "U"
        if (map[xgrid + xdir][ygrid] == " "):
            self.rect.x += xdir * enemymovespeed
            freebool = True
        if (map[xgrid][ygrid + ydir] == " "):
            self.rect.y += ydir * enemymovespeed
            freebool= True
        if (not freebool):
            if (map[xgrid - xdir][ygrid] == " "):
                self.rect.x -= xdir * enemymovespeed
            if (map[xgrid][ygrid - ydir] == " "):
                self.rect.y -= ydir * enemymovespeed
            
        print("y" + str(ygrid),"x" + str(xgrid) + dir)
        dx = pacman.rect.x - self.rect.x
        dy = pacman.rect.y - self.rect.y
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()

# Create a list of tiles for the walls
wall_list = pygame.sprite.Group()
pointpuck_list = pygame.sprite.Group()

player_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()

# Create walls on the screen (each tile is 20 x 20 so alter cords)
for y in range(maxsizey):
    for x in range (maxsizex):
        if map[x][y] == "#":
            my_wall = tile(BLUE, 20, 20, x*20, y *20)
            wall_list.add(my_wall)
            all_sprites_list.add(my_wall)
        elif map[x][y] == "|":
            if y > maxsizey / 2:
                my_wall = tile(DARKGRAY, 20, 10, x*20, (y *20)+10)
            else:
                my_wall = tile(DARKGRAY, 20, 10, x*20, (y *20))
            all_sprites_list.add(my_wall)
            
        elif map[x][y] == "_":
            if x > maxsizex / 2:
                my_wall = tile(DARKGRAY, 10, 20, x*20 + 10, (y *20))
            else:
                my_wall = tile(DARKGRAY, 10, 20, x*20, (y *20))
            all_sprites_list.add(my_wall)

        elif map[x][y] == "o":
            my_pp = pointpuck(WHITE, 8,8,x*20 + 6 ,y*20 + 6)
            all_sprites_list.add(my_pp)
            pointpuck_list.add(my_pp)

        elif map[x][y] == "e":            
            enemy = enemy(RED,10,10,x*20,y*20)
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)

pacman = player(YELLOW,10,10,20,20)
all_sprites_list.add(pacman)
player_list.add(pacman)

high = 0


font = pygame.font.Font('freesansbold.ttf', 16) 
pointspawncounter = 0
### -- Game Loop
done = False
#while not done:
while not done:
    while pacman.lives >= 1:
        # -- user input and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.player_speed_update(-1,0)
                elif event.key == pygame.K_RIGHT:
                    pacman.player_speed_update(1,0)
                if event.key == pygame.K_UP:
                    pacman.player_speed_update(0,-1)
                elif event.key == pygame.K_DOWN:
                    pacman.player_speed_update(0,1)


        # -- Game Logic goes after this comment
        if pointspawncounter <= pointspawnfrequency:
            pointspawncounter+= 1
            if pointspawncounter == pointspawnfrequency:            
                puckspawned = False
                while not puckspawned:
                    xpos = random.randrange(0,maxsizex)
                    ypos = random.randrange(0,maxsizey)
                    if map[xpos][ypos] == " ":
                        puckspawned = True
                        pointspawncounter = 0
                        my_pp = pointpuck(WHITE, 8,8,xpos*20 + 6 ,ypos*20 + 6)
                        all_sprites_list.add(my_pp)
                        pointpuck_list.add(my_pp)
                
                
        # -- check for collision between pacman and walls
        player_collide_list = pygame.sprite.spritecollide(pacman, wall_list, False)
        for foo in player_collide_list:
            #pacman.player_speed_update(0, 0)
            pacman.rect.x = pacman_old_x
            pacman.rect.y = pacman_old_y

        player_collide_list = pygame.sprite.spritecollide(pacman, pointpuck_list, True)
        for foo in player_collide_list:
            pacman.score += 1
        
        player_collide_list = pygame.sprite.spritecollide(pacman, enemy_list, False)
        for foo in player_collide_list:
            pacman.lives -= 1
            
        if pacman.rect.y > (maxsizey*20):
            pacman.rect.y = -11
        elif pacman.rect.y <= 0 - 11:
            pacman.rect.y = (maxsizey*20)

        if pacman.rect.x >= (maxsizex*20):
            pacman.rect.x = - 11
        elif pacman.rect.x <= 0 - 11:
            pacman.rect.x = (maxsizex*20)
            
        pacman_old_x = pacman.rect.x
        pacman_old_y = pacman.rect.y

        # -- screen background is BLACK

        screen.fill(BLACK)

        # -- Draw here
        all_sprites_list.draw(screen)

        all_sprites_list.update()

        text = font.render(" | score: " + str(pacman.score) \
                           + " | lives: " + str(pacman.lives) + " | ", True, WHITE)
        textRect = text.get_rect()
        textRect.center = (maxsizex * 20 // 2, 20 // 2)
        screen.blit(text,textRect)

        # -- flip display to reveal new position of objects
        pygame.display.flip()

        # - the clock ticks over
        clock.tick(60)
    while pacman.lives < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pacman.lives = startinglives
                    for foo in pointpuck_list:
                        foo.kill()
                    pacman.score = 0
                    pacman.rect.x = 20
                    pacman.rect.y = 20
                    for y in range(maxsizey):
                        for x in range (maxsizex):
                            if map[x][y] == "e":
                                enemy.rect.x = x * 20
                                enemy.rect.y = y * 20
                    
        screen.fill(BLACK)

        if high < pacman.score:
            high = pacman.score
        
        GOtext = font.render("Game Over", True, WHITE)
        GOtextRect = GOtext.get_rect()
        GOtextRect.center = (maxsizex * 20 // 2, 20 // 2)        

        text = font.render(" | score: " + str(pacman.score)+ " highscore: " + str(high) + " | ", True, WHITE)
        textRect = text.get_rect()
        textRect.center = (maxsizex * 20 // 2, maxsizey * 20 // 2)        

        Rtext = font.render("press space to restart", True, WHITE)
        RtextRect = Rtext.get_rect()
        RtextRect.center = (maxsizex * 20 // 2, maxsizey * 20 // 2 + 30)

        screen.blit(Rtext,RtextRect)
        screen.blit(text,textRect)
        screen.blit(GOtext,GOtextRect)

        # -- flip display to reveal new position of objects
        pygame.display.flip()

        # - the clock ticks over
        clock.tick(60)

# - end of game loop

pygame.quit()
