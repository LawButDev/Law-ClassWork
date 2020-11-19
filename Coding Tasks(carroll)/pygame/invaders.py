import pygame
import random
import math
# -- global constants
xrate = 1
yskip = 16
xoffset = 0
yoffset = 0
enemyshootchance = 10

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (640,450)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Invaders")

# --- Class Definitions
class barrier(pygame.sprite.Sprite):
    def __init__(self,width,height,size):
        super().__init__()
        #self.image=pygame.Surface([640,450])
        #self.rect = self.image.get_rect()
        barrier = [\
            "    ########    ",
            "   ##########   ",
            "  ############  ",
            " ############## ",
            " ############## ",
            " ############## ",
            " ############## ",
            " #####    ##### ",
            " ###        ### "]
        for y in range(9):
            for x in range(16):
                if barrier[y][x] == "#":
                    block = pixel(width - 8 * size + x * size,height + y * size,size)
                    barrier_list.add(block)
                    all_sprites_group.add(block)
class pixel(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        super().__init__()
        self.image=pygame.Surface([size,size])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x + size // 2
        self.rect.y = y + size // 2
    def update(self):
        self.fillervar = 0
        
        
        
        
# -- define the class snow which is a sprite
class Invader(pygame.sprite.Sprite):
    #defines the constructor for the snow sprites
    def __init__(self,color,x,y,width,height,speed):
        #call in the constructer for sprites
        super().__init__()
        #creates a sprite and fill it in with color
        self.image=pygame.Surface([width,height])
        picture = pygame.image.load("invader.png").convert()
        picture = pygame.transform.scale(picture, (width, height))
        self.image = picture
        #self.image.fill(color)
        #sets the position of the sprite
        self.speed = speed
        self.startx = x
        self.starty = y
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.width = width
        self.height = height
        self.rect.y = 0 - random.randrange(0,50)        
    def fire_bullet(self):
        bullet = Bullet(RED,self.rect.x+self.width/2,self.rect.y+self.width/2,-1)
        enemy_bullet_group.add(bullet)
        all_sprites_group.add(bullet)
    def update(self):
        self.rect.x = self.startx + xoffset
        self.rect.y = self.starty + yoffset
        shotchance = random.randrange(0,5000)
        if enemyshootchance >= shotchance:
            self.fire_bullet()
        #self.rect.y += self.speed
        #if self.rect.y >= 450:
        #    self.rect.x = random.randrange(0,600)
        #    self.rect.y = 0

class Player(pygame.sprite.Sprite):
    #defines the constructor for the snow sprites
    def __init__(self,color,width,height):
        #call in the constructer for sprites
        super().__init__()
        #creates a sprite and fill it in with color
        self.image=pygame.Surface([width,height])
        picture = pygame.image.load("player.png")
        picture = pygame.transform.scale(picture, (width, height))
        self.image = picture
        #sets the position of the sprite
        self.speed = 0
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 450-height
        self.width = width
        self.bullet_count=50
        self.score = 0
        #resets player lives
        self.lives = 3
    def player_set_speed(self,newspeed):
        self.speed = newspeed
    def fire_bullet(self):
        self.bullet_count -= 1
        bullet = Bullet(RED,self.rect.x+self.width/2,self.rect.y+self.width/2,1)
        bullet_group.add(bullet)
        all_sprites_group.add(bullet)
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 640-self.speed - self.width:
            self.rect.x = 640 - self.width
        if self.rect.x < 0+self.speed:
            self.rect.x = 0

class Bullet(pygame.sprite.Sprite):
    #defines the constructor for the bullet
    def __init__(self,color,x,y,direction):
        super().__init__()
        self.image=pygame.Surface([2,2])
        #self.image.fill(color)
        self.image.fill(WHITE)
        self.speed = 2
        self.rect = self.image.get_rect()
        self.rect.x = x - 1
        self.rect.y = y - 1
        self.width = 2
        self.direction = direction
    def update(self):
        self.rect.y -= self.speed * self.direction
        

# -- Exit game flag set to false
done = False

# creates a list of the invader blocks
invaders_group = pygame.sprite.Group()

#creates a list of all sprites
all_sprites_group = pygame.sprite.Group()

#creates a list of all bullet sprites
bullet_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

barrier_list = pygame.sprite.Group()

enemy_bullet_group = pygame.sprite.Group()

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

invcentx = 320
invcenty = 64
#creates the invaders
for y in range(4):
            for x in range(10):
                my_invader = Invader(BLUE,invcentx - 5 *32 + x * 32,invcenty - 2 * 32 + y * 32,16,16,1) # invaders are white and 5by5
                invaders_group.add(my_invader) # adds the new invader to the invader sprite group
                all_sprites_group.add(my_invader)
                
#creates the player
player = Player(YELLOW,32,16)
all_sprites_group.add(player)
player_group.add(player)

barrier1 = barrier(390,350,4)
barrier2 = barrier(250,350,4)
barrier3 = barrier(110,350,4)
barrier4 = barrier(530,350,4)
#all_sprites_group.add(barrier)

font = pygame.font.Font('freesansbold.ttf', 16) 

### -- Game Loop
direc = 1
while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.player_set_speed(-3)
            elif event.key == pygame.K_RIGHT:
                player.player_set_speed(3)
            if event.key == pygame.K_UP:
                player.fire_bullet()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.player_set_speed(0)


    # -- Game Logic goes after this comment
    all_sprites_group.update()

    # -- invader movement logic
    if (invcentx + xoffset + (direc * (32 * 5)) <= 0) :
        yoffset += yskip
        direc = 1
    elif(invcentx + xoffset + (direc * (32 * 5)) >= 640) :
        yoffset += yskip
        direc = -1
    xoffset += xrate * direc
    #--detects when the invader hits a player
    player_hit_group=pygame.sprite.spritecollide(player,invaders_group,True)
    for foo in player_hit_group:
        player.lives -= 1

    #--a bullet hits an invader
    Ehit = pygame.sprite.groupcollide(
        bullet_group, invaders_group,
        True, True)
    for foo in Ehit:
        player.score += 5

    #-- a bullet hits the player
    Phit = pygame.sprite.groupcollide(
        enemy_bullet_group, player_group,
        True, False)
    for foo in Phit:
        player.lives -= 1
            
    #when a player shoots a barrier
    #for i in range( 0, len(list(bullet_group))):
    #    wall_hit_group=pygame.sprite.spritecollide(list(bullet_group)[i],barrier_list,True)
    #for i in range( 0, len(list(barrier_list))):
    #    wall_hit_group=pygame.sprite.spritecollide(list(barrier_list)[i],bullet_group,True)

    hits = pygame.sprite.groupcollide(
            bullet_group, barrier_list,
            True, True)
    hits = pygame.sprite.groupcollide(
            enemy_bullet_group, barrier_list,
            True, True)
    
    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    all_sprites_group.draw(screen)

    text = font.render(" | lives: " + str(player.lives) \
                       + " | bullets: " + str(player.bullet_count)\
                       + " | score: " + str(player.score) + " | ", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (640 // 2, 20 // 2)
    screen.blit(text,textRect)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
