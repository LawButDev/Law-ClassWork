import pygame
import random
import math
# -- global constants

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
# -- define the class snow which is a sprite
class Invader(pygame.sprite.Sprite):
    #defines the constructor for the snow sprites
    def __init__(self,color,width,height,speed):
        #call in the constructer for sprites
        super().__init__()
        #creates a sprite and fill it in with color
        self.image=pygame.Surface([width,height])
        self.image = pygame.image.load("invader.png")
        #self.image.fill(color)
        #sets the position of the sprite
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.rect.y = 0 - random.randrange(0,50)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.x = random.randrange(0,600)
            self.rect.y = 0

class Player(pygame.sprite.Sprite):
    #defines the constructor for the snow sprites
    def __init__(self,color,width,height):
        #call in the constructer for sprites
        super().__init__()
        #creates a sprite and fill it in with color
        self.image=pygame.Surface([width,height])
        self.image.fill(color)
        #sets the position of the sprite
        self.speed = 0
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 450-height
        self.width = width
        self.bullet_count=50
        self.score = 0
        #resets player lives
        self.lives = 5
    def player_set_speed(self,newspeed):
        self.speed = newspeed
    def fire_bullet(self):
        self.bullet_count -= 1
        bullet = Bullet(RED,self.rect.x+self.width/2,self.rect.y+self.width/2)
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
    def __init__(self,color,x,y):
        super().__init__()
        self.image=pygame.Surface([2,2])
        self.image.fill(color)
        self.speed = 2
        self.rect = self.image.get_rect()
        self.rect.x = x - 1
        self.rect.y = y - 1
        self.width = 2
    def update(self):
        self.rect.y -= self.speed
        

# -- Exit game flag set to false
done = False

# creates a list of the invader blocks
invaders_group = pygame.sprite.Group()

#creates a list of all sprites
all_sprites_group = pygame.sprite.Group()

#creates a list of all bullet sprites
bullet_group = pygame.sprite.Group()

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

#creates the invaders
max_invaders = 10 # caps the invaders to 50
for x in range(max_invaders):
    my_invader = Invader(BLUE,10,10,1) # invaders are white and 5by5
    invaders_group.add(my_invader) # adds the new invader to the invader sprite group
    all_sprites_group.add(my_invader) # adds the new invaders to the group of all sprites

#creates the player
player = Player(YELLOW,10,10)
all_sprites_group.add(player)

font = pygame.font.Font('freesansbold.ttf', 16) 

### -- Game Loop

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

    #--detects when the invader hits a player
    player_hit_group=pygame.sprite.spritecollide(player,invaders_group,True)
    for foo in player_hit_group:
        player.lives -= 1

    #--a bullet hits an invader
    for i in range( 0, len(list(bullet_group))):
        invader_hit_group=pygame.sprite.spritecollide(list(bullet_group)[i],invaders_group,True)
        for foo in invader_hit_group:
            player.score += 5
        
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
