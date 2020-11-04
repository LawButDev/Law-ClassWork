import pygame
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
pygame.display.set_caption("House")

# -- Exit game flag set to false
done = False

sun_x=40
sun_y=100
bg_r = 5
bg_g = 5
bg_b = 0

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # -- Game Logic goes after this comment
    sun_x = sun_x+5
        
    if sun_x >= 640:
        sun_x = 0
        
    if sun_x <= 320:
        sun_y -= 1
        bg_r += 0.75
        bg_g += 0.5
    else:
        sun_y += 1
        bg_r -= 0.75
        bg_g -= 0.5
    
    # -- screen background is BLACK

    BG = (bg_r,bg_g,bg_b)
    screen.fill(BG)

    # -- Draw here
    pygame.draw.rect(screen,BLUE,(220,165,200,150))
    pygame.draw.circle(screen, YELLOW, (sun_x,sun_y),40,0)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
