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
pygame.display.set_caption("PONG")

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # -- Game Logic goes after this comment

    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    pygame.draw.rect(screen,BLUE,(220,165,200,150))
    pygame.draw.circle(screen, YELLOW, (40,100),40,0)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
