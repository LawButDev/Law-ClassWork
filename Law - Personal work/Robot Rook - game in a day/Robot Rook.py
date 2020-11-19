import pygame
import random
# -- global constants
tilesize = 32
gravity = 1
playerspeed = 3
enemyspeed = 2
playerjump = 15
timelimit = 30
coinlimit = 10
coinscore = 1

map = [\
    "########################",
    "#               #      #",
    "#               #      #",
    "#               #      #",
    "#               #      #",
    "#     <===>     #      #",
    "#            <=]#[=>   #",
    "#                      #",
    "#               e      #",
    "#  e       <==========]#",
    "#[====>                #",
    "#      e               #",
    "#[====================]#"]

MM = [\
    "           {}           ",
    "          {rr}          ",
    "         {rrrr}         ",
    "         ######         ",
    "         #^##^#         ",
    "         #|##|#         ",
    "         #|##|#         ",
    "=========#V##V#=========",
    "########################",
    "#####^############^#####",
    "#####|############|#####",
    "#####V############V#####",
    "########################"]

mapsizex = 24
mapsizey = 13


# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
LIGHTBLUE = ( 150,150,255)
YELLOW = (255,255,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (mapsizex * tilesize,mapsizey * tilesize)
screen = pygame.display.set_mode(size)

# -- sprite calls

fullstone = pygame.transform.scale(pygame.image.load("fullwall.png").convert(), (tilesize,tilesize))
fullplank = pygame.transform.scale(pygame.image.load("fullplank.png").convert(), (tilesize,tilesize))
leftplank = pygame.transform.scale(pygame.image.load("leftplank.png").convert(), (tilesize,tilesize))
rightplank = pygame.transform.scale(pygame.image.load("rightplank.png").convert(), (tilesize,tilesize))
lefttrans = pygame.transform.scale(pygame.image.load("lefttrans.png"), (tilesize,tilesize))
righttrans = pygame.transform.scale(pygame.image.load("righttrans.png"), (tilesize,tilesize))
background = pygame.transform.scale(pygame.image.load("background.png").convert(), (tilesize,tilesize))
playerimg = (pygame.transform.scale(pygame.image.load("playerL.png"), (int(tilesize * 0.8),int(tilesize * 0.8))),pygame.transform.scale(pygame.image.load("playerR.png"), (int(tilesize * 0.8),int(tilesize * 0.8))))
enemyimg = (pygame.transform.scale(pygame.image.load("enemyL.png"), (int(tilesize * 0.8),int(tilesize * 0.8))),pygame.transform.scale(pygame.image.load("enemyR.png"), (int(tilesize * 0.8),int(tilesize * 0.8))))
windowimg = (pygame.transform.scale(pygame.image.load("windowB.png"), (int(tilesize * 1),int(tilesize * 1))),pygame.transform.scale(pygame.image.load("windowM.png"), (int(tilesize * 1),int(tilesize * 1))),pygame.transform.scale(pygame.image.load("windowT.png"), (int(tilesize * 1),int(tilesize * 1))))
roofimg = (pygame.transform.scale(pygame.image.load("roofL.png"), (int(tilesize * 1),int(tilesize * 1))),pygame.transform.scale(pygame.image.load("fullroof.png"), (int(tilesize * 1),int(tilesize * 1))),pygame.transform.scale(pygame.image.load("roofR.png"), (int(tilesize * 1),int(tilesize * 1))))
coinimg = pygame.transform.scale(pygame.image.load("coin.png"), (int(tilesize * 0.5),int(tilesize * 0.5)))
topbrick = pygame.transform.scale(pygame.image.load("topbrick.png"), (int(tilesize *1),int(tilesize * 1)))
logoimg = pygame.transform.scale(pygame.image.load("logo.png"),(tilesize *12, tilesize *6))


# Create a list of all sprites
all_sprites_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
back_sprites_list = pygame.sprite.Group()
platforms = list()
player_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
MM_sprites_group = pygame.sprite.Group()

# -- Title of new window/screen
pygame.display.set_caption("Robot Rook")

# -- class definitions
class platform(pygame.sprite.Sprite):
    # Define the constructor for the wall
    def __init__(self, sprite, size, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        # Create a sprite and fill it with colour
        self.image = pygame.Surface([size*tilesize,size*tilesize],pygame.SRCALPHA)
        self.image = sprite
        self.rect = self.image.get_rect()
        # Set the position of the wall's attributes
        self.rect.x = x_ref
        self.rect.y = y_ref
class coin(pygame.sprite.Sprite):
    def __init__(self, sprite, size, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        self.image = pygame.Surface([int(size*tilesize),int(size*tilesize)],pygame.SRCALPHA)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x_ref
        self.rect.y = y_ref

class logo(pygame.sprite.Sprite):
    def __init__(self, x_ref, y_ref):
        # Call the sprite constructor
        super().__init__()
        self.image = pygame.Surface([int(12*tilesize),int(6*tilesize)],pygame.SRCALPHA)
        self.image = logoimg
        self.rect = self.image.get_rect()
        self.rect.x = x_ref
        self.rect.y = y_ref
        self.rect.center = (x_ref,y_ref)

#class Character(Block):
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([int(tilesize * 0.8),int(tilesize * 0.8)],pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image = enemyimg[0]
        self.rect.x = x_ref
        self.rect.y = y_ref
        (self.dx, self.dy) = speed
        self.is_falling = True
        self.jumps = 2
        self.leftbool = False
        self.rightbool = False
        self.direction = -1
        self.gridx = 0
        self.gridy = 0

    def update(self, platforms):
        self.is_falling = True
        for platform in platforms:
            if self.is_on(platform):
                self.rect.bottom = platform.rect.top
                self.dy = 0
                self.jumps = 2
                self.is_falling = False

        if self.is_falling:
            self.gravity()
        self.gridx = self.rect.x // tilesize
        self.gridy = self.rect.y // tilesize
        if map[self.gridy][self.gridx + self.direction] != "#" and map[self.gridy + 1][self.gridx + self.direction] != " ":
            self.dx = self.direction * enemyspeed
        else:
            self.direction= self.direction * -1
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.direction == -1:
            self.image = enemyimg[0]
        elif self.direction == 1:
            self.image = enemyimg[1]

    def is_on(self, platform):
        return (pygame.Rect(self.rect.x, self.rect.y + self.dy + 1, # +1
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dy >= 0 and self.rect.y + int(tilesize * 0.8) // 2 <= platform.rect.y)

    def left(self):
        self.dx = -enemyspeed
        self.image = enemyimg[0]

    def right(self):
        self.dx = enemyspeed
        self.image = enemyimg[1]

    def stop_x(self):
        self.dx = 0

    def gravity(self):
        self.dy += gravity
        
#class Character(Block):
class Character(pygame.sprite.Sprite):
    def __init__(self, speed,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([int(tilesize * 0.8),int(tilesize * 0.8)],pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image = playerimg[0]
        self.rect.x = x_ref
        self.rect.y = y_ref
        (self.dx, self.dy) = speed
        self.is_falling = True
        self.jumps = 2
        self.leftbool = False
        self.score = 0
        self.rightbool = False

    def update(self, platforms):
        self.is_falling = True
        for platform in platforms:
            if self.is_under(platform):
                self.rect.top = platform.rect.bottom
            if self.is_on(platform):
                self.rect.bottom = platform.rect.top
                self.dy = 0
                self.jumps = 2
                self.is_falling = False
            elif self.is_right(platform):
                self.rect.right = platform.rect.left
                self.jumps = 1
                self.dx = 0            
            elif self.is_left(platform):
                self.rect.left = platform.rect.right
                self.jumps = 1
                self.dx = 0

        if self.is_falling:
            self.gravity()
        self.rect.x += self.dx
        self.rect.y += self.dy

    def is_on(self, platform):
        return (pygame.Rect(self.rect.x, self.rect.y + self.dy + 1, # +1
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dy >= 0 and self.rect.y + int(tilesize * 0.8) // 2 <= platform.rect.y)
    def is_under(self, platform):
        return (pygame.Rect(self.rect.x, self.rect.y + (self.dy - 1), # +1
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dy <= 0 and self.rect.top >= platform.rect.center[1])
    
    def is_right(self, platform):
        return (pygame.Rect(self.rect.x + self.dx + 1,self.rect.y,  # +1
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dx >= 0 and self.rect.x + int(tilesize * 0.8) // 2 <= platform.rect.x)
    def is_left(self, platform):
        return (pygame.Rect(self.rect.x + (self.dx - 1),self.rect.y,  # +1
                            self.rect.width, self.rect.height)
                .colliderect(platform.rect) and self.dx <= 0 and self.rect.x + int(tilesize * 0.8) // 2 >= platform.rect.x)

    def left(self):
        self.dx = -playerspeed
        self.image = playerimg[0]

    def right(self):
        self.dx = playerspeed
        self.image = playerimg[1]

    def stop_x(self):
        self.dx = 0

    def jump(self):
        #if self.dy == 0:
        if self.jumps > 0:
            self.jumps -= 1
            self.dy = -playerjump

    def gravity(self):
        self.dy += gravity

# -- Exit game flag set to false
done = False
maindone = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()



def key_down(event, character):
    if event.key == pygame.K_LEFT:
        character.stop_x()
        character.left()
        character.leftbool = True
    if event.key == pygame.K_RIGHT:
        character.stop_x()
        character.right()
        character.rightbool = True
    if event.key == pygame.K_UP:
        character.jump()

def key_up(event, character):
    if event.key == pygame.K_LEFT:
        character.leftbool = False
    if event.key == pygame.K_RIGHT:
        character.rightbool = False
    if event.key in (pygame.K_LEFT, pygame.K_RIGHT) and character.rightbool == False and character.leftbool == False:
        character.stop_x()
font = pygame.font.Font('freesansbold.ttf',tilesize)

def main():
    start_ticks=pygame.time.get_ticks() #starter tick
    maindone = False
    all_sprites_list.empty
    wall_list.empty
    back_sprites_list.empty()
    platforms.clear()
    player_list.empty()
    enemy_list.empty()
    coins_group.empty()
    for foo in coins_group:
        foo.kill()
    for foo in all_sprites_list:
        foo.kill()  
    for foo in player_list:
        foo.kill()          
    for foo in enemy_list:
        foo.kill()
    for y in range(mapsizey):
        for x in range (mapsizex):
            if map[y][x] == "#":
                new_wall = platform(fullstone, 1, x*tilesize, y *tilesize)
                wall_list.add(new_wall)
                platforms.append(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == "[":
                new_wall = platform(leftplank, 1, x*tilesize, y *tilesize)
                wall_list.add(new_wall)
                platforms.append(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == "]":
                new_wall = platform(rightplank, 1, x*tilesize, y *tilesize)
                wall_list.add(new_wall)
                platforms.append(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == ">":
                new_back = platform(background,1, x*tilesize,y*tilesize)
                back_sprites_list.add(new_back)
                new_wall = platform(lefttrans, 1, x*tilesize, y *tilesize)
                #wall_list.add(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == "c":
                new_back = platform(background,1, x*tilesize,y*tilesize)
                back_sprites_list.add(new_back)
                new_coin = coin(coinimg, 0.5, x*tilesize, y *tilesize)
                coins_group.add(new_coin)
                all_sprites_list.add(new_coin)
            elif map[y][x] == "<":
                new_back = platform(background,1, x*tilesize,y*tilesize)
                back_sprites_list.add(new_back)
                new_wall = platform(righttrans, 1, x*tilesize, y *tilesize)
                #wall_list.add(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == "=":
                new_wall = platform(fullplank, 1, x*tilesize, y *tilesize)
                wall_list.add(new_wall)
                platforms.append(new_wall)
                all_sprites_list.add(new_wall)
            elif map[y][x] == "e":
                new_back = platform(background,1, x*tilesize,y*tilesize)
                back_sprites_list.add(new_back)
                new_enemy = Enemy((0,0),x*tilesize,y*tilesize)
                enemy_list.add(new_enemy)
            else:
                new_back = platform(background,1, x*tilesize,y*tilesize)
                back_sprites_list.add(new_back)

    for x in range(coinlimit):
        xpos = random.randrange(0,mapsizex)
        ypos = random.randrange(0,mapsizey)
        while map[ypos][xpos] != " ":
            xpos = random.randrange(0,mapsizex)
            ypos = random.randrange(0,mapsizey)
        
        new_coin = coin(coinimg, 0.5, xpos*tilesize, ypos *tilesize) 
        all_sprites_list.add(new_coin) 
        coins_group.add(new_coin)

                
    # -- instantiates player
    hero = Character((0,0),tilesize*(mapsizex//2),tilesize*(mapsizey//2))
    #all_sprites_list.add(hero)
    player_list.add(hero)
    maindone = False
    while not maindone:
        time = int(timelimit - (pygame.time.get_ticks()-start_ticks)/1000)
        if time <= 0:
            maindone = True
            global win
            win = False
        elif not(coins_group):
            global highscore
            if highscore <= hero.score:
                highscore = hero.score
            maindone = True
        # -- user input and controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                key_down(event, hero)
            elif event.type == pygame.KEYUP:
                key_up(event, hero)


        # -- Game Logic goes after this comment
        player_collide_list = pygame.sprite.spritecollide(hero, coins_group, True)
        for foo in player_collide_list:
            coins_group.remove(foo)
            hero.score += coinscore * time
        player_collide_list = pygame.sprite.spritecollide(hero, enemy_list, True)
        for foo in player_collide_list:
            maindone = True

        # -- screen background is BLACK

        screen.fill(BLACK)

        # -- Draw here
        back_sprites_list.draw(screen)
        all_sprites_list.draw(screen)
        all_sprites_list.update()
        player_list.draw(screen)
        player_list.update(platforms)
        enemy_list.draw(screen)
        enemy_list.update(platforms)

        # -- text ui
        
        text = font.render(" | SCORE: " + str(hero.score) \
                               + " | TIME: " + str(time) + " | ", True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((mapsizex * tilesize) // 2,\
                           2*tilesize // 2)
        screen.blit(text,textRect)

        # -- flip display to reveal new position of objects
        pygame.display.flip()

        # - the clock ticks over
        clock.tick(60)

# -- instantiates main menu
for y in range(mapsizey):
        for x in range (mapsizex):
            if MM[y][x] == "#":
                new_wall = platform(fullstone, 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "^":
                new_wall = platform(windowimg[2], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "|":
                new_wall = platform(windowimg[1], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "V":
                new_wall = platform(windowimg[0], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "{":
                new_wall = platform(roofimg[0], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "r":
                new_wall = platform(roofimg[1], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "}":
                new_wall = platform(roofimg[2], 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
            elif MM[y][x] == "=":
                new_wall = platform(topbrick, 1, x*tilesize, y *tilesize)
                MM_sprites_group.add(new_wall)
                
new_logo = logo(((mapsizex // 2) * tilesize), ((mapsizey // 2) * tilesize))
MM_sprites_group.add(new_logo)
        

### -- Game Loop
maindone = True
highscore = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main()
    screen.fill(LIGHTBLUE)

    MM_sprites_group.draw(screen)
    MM_sprites_group.update()
    
        
    text = font.render(" High Score: " + str(highscore), True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((mapsizex * tilesize) // 2,\
                       mapsizey * tilesize - 2*tilesize // 2)
    screen.blit(text,textRect)

    text2 = font.render(" Press space to start ", True, WHITE)
    text2Rect = text2.get_rect()
    text2Rect.center = ((mapsizex * tilesize) // 2,\
                       mapsizey * tilesize - 4*tilesize // 2)
    screen.blit(text2,text2Rect)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()
