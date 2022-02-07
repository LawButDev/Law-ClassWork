dist = math.sqrt((abs(player.center.x-start[0]))**2 + (player.center.y-start[1])**2)
    if dist < mindis:
        colx = start[0]
        coly = start[1]
        mindis = dist
        sprite = col.sprite
        loc = -1
        if ((start[0] == col.leftside) or (start[0] == col.rightside)) and ((start[1] == col.top) or (start[1] == col.bottom)):
            loc = 0
        else if ((start[0] == col.leftside) or (start[0] == col.rightsize - 1)):
            loc = abs(int(start[1]-col.top))
        else if ((start[1] == col.top) or (start[1] == col.bottom - 1)):
            loc = abs(int(start[0]-col.leftside))
        else:
            loc = 32
        corsprite <= subimage(sprite, (loc, 0, 1, 64))
    end if

dispsprite <= scale(corsprite,(2,int(projheight)*2))
sprite_cont <= Container((0,0),(2, int(projheight)*2))
screen.draw(dispsprite,(2*f,1*(size[1]//2-projheight//1)),sprite_cont)



getinput()
if input = ("w" or forwardarrow):
    moveforward()
else if input = ("s" or backarrow):
    moveback()
getinput()
end if
if input = ("a" or leftarrow):
    moveleft()
else if input = ("d" or rightarrow):
    moveright()
end if


def moveplayer(relx,rely,rot):
    xchange,ychange <= 0
    //rely handling (where player is facing)
    xchange += rely * (cos(rot))
    ychange += rely * (sin(rot))

    xchange += relx * (cos(rot+90))
    ychange += relx * (sin(rot+90))

    player.x += xchange
    player.y += ychange
end procedure

def shoot():
    hitFlag <= False
    for enm in enemyList[]
        collidedline = enm.collideline((player.x,player.y),(player.x+xdiff,player.y+ydiff))
        if collidedline:
            hitFlag <= True
            for obs in mapList[]
                if blockcollide = obs.collideline((player.x,player.y),(player.x+xdiff
            next
        end if
    next
end procedure

def deathRequest(shooterID,ShotID):
        #placeholder logic to represent external function to respawn player
        ShotID.RespawnHandler(spawnpoints.randomspawn())

        scoreboard[shooterID].Addkill(1)
        scoreboard[shotID].AddDeath(1)
        
end procedure




import pygame
import math
# -- global constants
size = [640,640]

cubesize = 64
pheight = cubesize // 2
pwidth = pheight // 4
FOV = 60
mossen = 0.25
projplane = (320,200)
planedist = int((projplane[0] // 2) / math.tan((FOV // 2) / (180 / math.pi)))
rayang = 60 / 320


playerspeed = 16
strafespeedmultiplyer = 0.8

mapgrid = ["##########",
           "#  #     #",
           "#        #",
           "#        #",
           "#        #",
           "#        #",
           "#        #",
           "#        #",
           "#        #",
           "##########"]
        


# -- class list definitions
debug_list = pygame.sprite.Group()
      
        


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
pygame.display.set_caption("Pseudo3D")

# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

# - instantiations

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        done = True


    # -- Game Logic goes after this comment

    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    debug_list.draw(screen)
    debug_list.update() 

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(60)

# - end of game loop

pygame.quit()







class player(pygame.sprite.Sprite):
    # initialiser
    def __init__(self,xpos,ypos,rotation):
        super().__init__()
        self.xpos = xpos # x coordinate
        self.ypos = ypos # y coordinate
        self.image = pygame.Surface([size[0] // 20, size[1] // 20], pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rot = rotation # rotation from north
        pygame.draw.polygon(self.image, (150,150,200,100), ((self.rect.center[0],self.rect.top),(self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom))) # draws triangle to be visible on screen
        self.rect.center = (self.xpos,self.ypos) # set centre of player to desired coordinates
        self.orgimage = self.image
        self.speed = playerspeed # forward speed
        self.strafespeed = int(playerspeed * strafespeedmultiplyer) # modifies speed for strafing


    def update(self):
        # - beginning of ray casting
        ray = 0
        while ray <= projplane[0]:
            temprot = self.rot - 30 + ((ray - 1) * rayang) # calculate the rotation of the ray within the Fov

            #angle correction
            if temprot <= 0:
                temprot += 360
            elif temprot >= 360:
                temprot -= 360
                    
            
            ray += 1


    def update(self):
        # mouse movement handling
        pygame.event.set_grab(True) # holds the mouse in place
        pygame.mouse.set_visible(False) # hides the mouse cursor
        delta_x, delta_y = pygame.mouse.get_rel() # gets relative position of mouse from last frame
        self.rot += float(-delta_x * mossen)
        if self.rot > 360:
            self.rot -= 360
        elif self.rot <= 0:
            self.rot += 360
        self.image = pygame.transform.rotate(self.orgimage, self.rot) # updates visualisation
        self.rect.center = (self.xpos,self.ypos)

        print(self.rot)

        self.gridx = self.rect.center[0] // 64
        self.gridy = self.rect.center[1] // 64
        # - beggining of ray casting
        ray = 0
        while ray <= projplane[0]:
            temprot = self.rot - 30 + ((ray - 1) * rayang)
            
            if temprot <= 0:
                temprot += 360
            elif temprot >= 360:
                temprot -= 360

            # -- wall detection
            ##  - horizontal
            if 0 < temprot and temprot <= 90:
                Ay = int(self.rect.center[1] / 64) * 64 - 1
                Ya = -cubesize
                Xadir = 1
                Xa = (Ya * math.tan(temprot * (math.pi / 180)))
            elif 90 < temprot and temprot <= 180:
                Ay = int(self.rect.center[1] / 64) * 64 + 64
                Ya = cubesize
                Xadir = -1
                Xa = (Ya / math.tan(temprot * (math.pi / 180)))
            elif 180 < temprot and temprot <= 270:
                Ay = int(self.rect.center[1] / 64) * 64 + 64
                Ya = cubesize
                Xadir = -1
                Xa = (Ya * math.tan(temprot * (math.pi / 180)))
            elif 270 < temprot and temprot <= 360:
                Ay = int(self.rect.center[1] / 64) * 64 - 1
                Ya = -cubesize
                Xadir = 1
                Xa = (Ya / math.tan(temprot * (math.pi / 180)))

            if temprot == 0: temprot += 1 / 10000
            
            Ax = self.rect.center[0] + (self.rect.center[1] - Ay) / math.tan((temprot) * (math.pi / 180))
            
            #Xa = (abs(Ya) / math.tan(temprot * (math.pi / 180)))

            

collided = False
Oldx = Ax
Oldy = Ay
while collided == False:
    Oldx += Xa
    Oldy += Ya
    if int(Oldy // cubesize) < 10 and int(Oldy // cubesize) >= 0 and int(Oldx // cubesize) < 10 and int(Oldx // cubesize) >= 0:
        if mapgrid[int(Oldy // cubesize)][int(Oldx // cubesize)] == "#":
            collided = True
    else: collided = True
if Oldx <= 0:
    Oldx = 0
if Oldy <= 0:
    Oldy = 0
if Oldx > 640:
    Oldx = 640
if Oldy > 640:
    Oldy = 640
            pygame.draw.line(screen, (255,255,255,175), (self.rect.center), (Oldx,Oldy))
                    
            
            ray += 1


corang = f*rayang - 30
dist = math.sqrt((abs(self.rect.center[0]-colx))**2 + (self.rect.center[1]-coly)**2)
cordist = math.cos(math.radians(corang))*dist
if cordist == 0: cordist += 0.000001
cordist = dist

#wall height calc based on distance to proj plane (projdist)
projheight = (64 / cordist) * projdist

#debug basic render of view using lines (needs to be rewritten to sprite) - since the porj plane must be doubled in size the height is doubled and x coord is doubled
pygame.draw.line(screen,(dcc // 6,dcc//3,dcc // 1,175),(2*f,1*(size[1]//2 - projheight // 1)),(2*f,1*(size[1]//2 + projheight // 1)),2)



self.xdif = 0
self.ydif = 0
    
#strafing angle correction calc
x_move = int(math.cos(math.radians(self.rot -90)) * (unit * pmm))
y_move = int(math.sin(math.radians(self.rot -90)) * (unit * pmm))
    
# -- left right movement
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    self.xdif += x_move
    self.ydif += y_move
elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    self.xdif -= x_move
    self.ydif -= y_move     

#standard movement angle correction calc
x_move = math.cos(math.radians(self.rot)) * (unit * pmm)
y_move = math.sin(math.radians(self.rot)) * (unit * pmm)

keys = pygame.key.get_pressed()
if keys[pygame.K_UP] or keys[pygame.K_w]:
    self.xdif += x_move
    self.ydif += y_move
elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
    self.xdif -= x_move
    self.ydif -= y_move

if self.xdif >= 0: self.dirx = 1
else: self.dirx = -1
if self.ydif >= 0: self.diry = 1
else: self.diry = -1

self.rect.x += self.xdif

self.rect.y += self.ydif



