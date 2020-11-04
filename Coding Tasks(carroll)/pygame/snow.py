import pygame
import random
import math
# -- global constants

# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (640,450)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Snow")

# --- Class Definitions
# -- define the class snow which is a sprite
class Snow(pygame.sprite.Sprite):
    #defines the constructor for the snow sprites
    def __init__(self,color,width,height,speed):
        #call in the constructer for sprites
        super().__init__()
        #creates a sprite and fill it in with color
        self.image=pygame.Surface([width,height])
        self.image.fill(color)
        #sets the position of the sprite
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,600)
        self.rect.y = random.randrange(0,400)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.x = random.randrange(0,600)
            self.rect.y = 0
        
        

# -- Exit game flag set to false
done = False

# creates a list of the snow blocks
snow_group = pygame.sprite.Group()

#creates a list of all sprites
all_sprites_group = pygame.sprite.Group()

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

#creates the snowflakes
max_flakes = 50 # caps the snowflakes to 50
for x in range(max_flakes):
    my_snow = Snow(WHITE,5,5,1) # snowflakes are white and 5by5
    snow_group.add(my_snow) # adds the new snowflake to the snowflake sprite group
    all_sprites_group.add(my_snow) # adds the new snowflakes to the group of all sprites
### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # -- Game Logic goes after this comment
    all_sprites_group.update()
        
    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    all_sprites_group.draw(screen)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
