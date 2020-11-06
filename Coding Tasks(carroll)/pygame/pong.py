import pygame
# -- global constants
ball_width = 20
og_ball_speed = 5
ball_speed_increase = 0.15

ball_speed = og_ball_speed

# - paddle definitions
padd_length = 15
padd_width = 60

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

# - pre game loop declerations

x_val = 150
y_val = 200

x_direction = ball_speed
y_direction = ball_speed

x_padd = 0
y_padd = 20

score = 0

font = pygame.font.Font('freesansbold.ttf', 32) 

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if y_padd >= 5:
            y_padd -= 5
    if keys[pygame.K_DOWN]:
        if y_padd <= 450 - padd_width - 5:
            y_padd += 5


    # -- Game Logic goes after this comment
    if (((x_padd <= x_val + ball_width) and (x_val <= x_padd + padd_length)) and ((y_padd <= y_val) and (y_val + ball_width <= y_padd + padd_width))):
        x_direction = (x_direction) * (-1)
        ball_speed += ball_speed_increase
        score += 1
    if x_val + ball_width >= 640:
        x_direction = -ball_speed
    elif x_val + ball_width <= 0:
        ball_speed = og_ball_speed
        x_direction = ball_speed
        y_direction = ball_speed
        x_val = 150
        y_val = 200
        score = 0
        ##if score >= 10:
            ##done = True
    if y_val + ball_width >= 450:
        y_direction = -ball_speed
    elif y_val <= 0:
        y_direction = ball_speed
    
    x_val += x_direction
    y_val += y_direction

    
    text = font.render(str(score), True, WHITE,BLACK)
    textRect = text.get_rect()
    textRect.center = (640 // 2, 450 // 2) 

    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    pygame.draw.rect(screen,BLUE,(x_val,y_val,ball_width,ball_width))

    # - paddles
    pygame.draw.rect(screen,WHITE,(x_padd,y_padd,padd_length,padd_width))

    screen.blit(text, textRect) 

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
