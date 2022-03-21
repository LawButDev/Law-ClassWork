



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



sprite = col.sprite
loc = -1
if ((start[0] == col.rect.left) or (start[0] == col.rect.right)) and ((start[1] == col.rect.top) or (start[1] == col.rect.bottom)):
    loc = 0
elif ((start[0] == col.rect.left) or (start[0] == col.rect.right - 1)):
    loc = abs(int(start[1]-col.rect.top))
elif ((start[1] == col.rect.top) or (start[1] == col.rect.bottom - 1)):
    loc = abs(int(start[0]-col.rect.left))
else:
    loc = 32

corsprite = pygame.Surface.subsurface(sprite, (loc, 0, 1, 64))


dispsprite = pygame.transform.scale(corsprite,(2,int(projheight)*2))
cont_rect = pygame.Rect((0,0),(2, int(projheight)*2))

screen.blit(dispsprite,(2*f,1*(size[1]//2-projheight//1)),cont_rect)




#floor render
pygame.draw.rect(screen,(100,100,100,255),(0,size[1]//2,size[0], size[1] // 2),0)

#ceilling render
pygame.draw.rect(screen,(0,0,100,255),(0,0,size[0], size[1] // 2),0)


dcc = max((255-((cordist)//2)**1), 10)
overlayline = pygame.Surface((2,int(projheight * 2)),pygame.SRCALPHA)
overlayline.fill((0,0,0,255-dcc))
screen.blit(overlayline,(2*f,1*(size[1]//2-projheight//1)))



class ent(pygame.sprite.Sprite):
    def __init__(self,x_ref,y_ref,x_size,y_size,sprite):
        super().__init__()
        self.type = "sprite"
        self.image = pygame.Surface((x_size,x_size),pygame.SRCALPHA)
        self.image.fill((70,150,200,255))
        self.x_size = x_size
        self.sprite = sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x_ref,y_ref)
        self.checkedthisframe = False
        self.firstray = 0
        self.firstdist = 0
        
        self.spritecentdist = math.sqrt((abs(PC.rect.center[0]-self.rect.center[0]))**2 + (abs(PC.rect.center[1]-self.rect.center[1]))**2)
        self.spritecentang = math.degrees((math.atan2((PC.rect.center[1]-self.rect.center[1]),(PC.rect.center[0]-self.rect.center[0])))%(2*math.pi))
    def update(self):
        self.spritecentdist = math.sqrt((abs(PC.rect.center[0]-self.rect.center[0]))**2 + (abs(PC.rect.center[1]-self.rect.center[1]))**2)
        self.spritecentang = math.degrees((math.atan2((-PC.rect.center[1]+self.rect.center[1]),(-PC.rect.center[0]+self.rect.center[0])))%(2*math.pi))
    def angcompare(self,num1,num2):
        num1div = num1 // 90
        num1rem = num1 % 90
        num2div = num2 // 90
        num2rem = num2 % 90
        if num1div >= 3: num1div = 0
        if num1div <= num2div and num1rem <= num2rem:
            return True
        else:
            return False


if col.type == "sprite":
    spriterot = anglecor(self.rot - 90)
    
    #concept of sprite / ray collisions is that the pixels are only one wide, therefor for every ray cast onto a sprite only the width of the sprite (i.e) 16 points must
    # checked, therefore if we know the equation of each line in y=mx+c we can loop through the 16 points on the sprite line and see if the two lines intersect
    #  from there you can find the pixel that point covers and render the sprite (only theoretical though, no fucking clue if itll work lol)
    
    
    clippedline = col.rect.clipline((self.rect.center[0],self.rect.center[1]),(self.rect.center[0] + xdif , self.rect.center[1] + ydif))
    if clippedline:
        #print("y = " + str(m) + "x + " + str(c))
        start,end = clippedline
        #pygame.draw.line(screen, (255,255,10,175), (start),(end),2)
        dist = math.sqrt(((self.rect.center[0]-start[0]))**2 + (self.rect.center[1]-start[1])**2)                        

        #print(spritecentang,self.rot%90)
        if True:#dist < spritedist: # and dist < col.x_size:
            spritedist = dist
            sprite = col.sprite
            spriteloc = 0

            #concept of new sprite render is to find the length of the line between the ray and the centre of the sprite, and if it is within the sprite boudnary working from there
            #this line finds the distance between the angles for later calculation
            angdif = abs(i - col.spritecentang) % 360
            #since the difference can be maximum 1
            if angdif >= 180 : angdif = 360 - angdif
            #swapped line to cause errors
            relspritedist = ((math.tan(math.radians(abs(i % 90 - col.spritecentang%90)))*col.spritecentdist))
            #relspritedist = abs((math.tan(math.radians(abs(angdif)))*col.spritecentdist))
            if relspritedist < 0: relspritedist = 0
            if relspritedist <= col.x_size // 2:
                #Render

i = 0
while i < len(sortedsprite):
    spritedist = sortedsprite[i][0]
    spritecorsprite = sortedsprite[i][1]
    spritecordist = spritedist
    spritecordist = math.cos(math.radians(corang))* spritedist
    if spritecordist == 0: spritecordist += 0.000001

    #sprite height calc based on distance to proj plane(porjdist)
    spriteprojheight = (unit/spritecordist)*projdist
    if spriteprojheight >= size[1] * maxsizemult : spriteprojheight = size[1] * maxsizemult

    spritedispsprite = pygame.transform.scale(spritecorsprite,(2,int(spriteprojheight)*2))
    spritecont_rect = pygame.Rect((0,0),(2, int(spriteprojheight)*2))
    
    if spritedist < cordist:
        screen.blit(spritedispsprite,(2*f,1*(size[1]//2-spriteprojheight//1)))#,spritecont_rect)
    i += 1

j = 0
sortedsprite = []

if len(spriteord) < 1:                
    j = 100
else:                
    sortedsprite.append((spriteord[0][0],spriteord[0][1]))
while j <= len(spriteord) - 1:
    stored = spriteord[j][0]
    inserted = False
    k = len(sortedsprite) - 1
    sortedsprite.append((9999,2333))
    while not inserted:
        if k >= 0:
            if stored > sortedsprite[k][0]:
                sortedsprite[k+1] = (sortedsprite[k][0],sortedsprite[k][1])
                sortedsprite[k] = (spriteord[j][0],spriteord[j][1])
                #sortedsprite[k] = (spriteord,0)
                k -= 1
            else:
                sortedsprite[k+1] = (spriteord[j][0],spriteord[j][1])
                inserted = True
        else: inserted = True
            
    j += 1









    ### START OF SERVER WORK ###

import socket
import sys
import pygame

#in order to ser this up the command 'ipconfig' must be run in command prompt
#the ipv4 adress must then be copied from that and put below

#put the ipv4 address here
server = "10.0.4.33"
#port is the standart port 5555 for simplicity
port = 5555

print("server: " + server, "port: " + str(port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

## tells the server to begin looking for a client that wants to connect
s.listen(2)
print("waiting for a connection, server started")

while True:
    conn, addr = s.accept()
    print("conntected to:", addr)



import socket

class Network:
    def __init__(self,ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(self.id)


    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass






from _thread import *

maxplayers = 15

players = []
currentplayers = []

def threaded_client(conn, player):
    reply = conn.send(str.encode(initialpack(player)))
    while True:
        indexval = currentplayers.index(player)
        toreply = players.copy()
        #print(indexval)
        toreply.pop(indexval)
        toreply.insert(0,players[indexval])
        #print(currentplayers)
        reply = toreply
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")                            

            if not data:
                print ("disconnected")
                break
            else:
                elsefiller = True
            conn.sendall(reply)

        except:
            break
    print("lost connection")
    indexval = currentplayers.index(player)
    players.pop(indexval)
    currentplayers.pop(indexval)
    conn.close()

while True:
    conn, addr = s.accept()
    print("conntected to:", addr)

    if (len(currentplayers) <= maxplayers):
        start_new_thread(threaded_client, (conn,currentPlayer))
        playercount += 1
        currentPlayer += 1

    for i in range(0,playercount):
        print("player " + str(i))




rawmap = open("map.txt","r")
rawmap.seek(0)
rawmapsize = rawmap.readline()
rawmapsize = rawmapsize.split(" ")
mapsize = (int(rawmapsize[0]),int(rawmapsize[1]))
savedmap = []
mapstr = ""
for line in range(mapsize[1] ):
    temp = rawmap.readline()
    savedmap.append(temp)
    mapstr += str(temp)# + "|")

spawnpoints = []
spawncount = 0
rawmap.seek(0)
for y in range (mapsize[1] ):
    ystr = savedmap[y]
    for x in range (mapsize[0]):
        if ystr[x] == "s":
            spawnpoints.append(str(x) + " " + str(y))
            spawncount += 1

def initialpack(playerint):
    return (str(mapsize[0]) + " " + str(mapsize[1]) + "/" + spawnpoints[random.randint(0,spawncount) - 1] + "/" + mapstr + "/" + str(playerint))

def threaded_client(conn, player):
    reply = conn.send(str.encode(initialpack(player)))



try:
    data = pickle.loads(conn.recv(2048))
    indexval = currentplayers.index(player)
                    

    if not data:
        print ("disconnected")
        break
    else:
        pog = True
    conn.sendall(pickle.dumps(reply))


cordtup = (PC.rect.x,PC.rect.y)
    playersent = pseudoplayer(PC.rect.x,PC.rect.y,PC.rot,clientid)
    playersent.todamage = todamage
    playersent.health = PC.health
    todamage = -1
    reply = interface.send(playersent)
    templayer = reply.pop(0)
    if templayer.health < 0:
        PC.rect.x = templayer.posx * unit
        PC.rect.y = templayer.posy * unit
        PC.rot = templayer.rotation
        PC.health = 100
    else:
        PC.health = templayer.health
    while len(activeplayers) < len(reply):
        placeholder = enemy(0,0,0,-1)
        debug_raycol.add(placeholder)
        debug_list.add(placeholder)
        activeplayers.append(placeholder)
        print("add")
    while len(activeplayers) > len(reply):
        activeplayers[-1].kill()
        activeplayers.pop()
        print("remove")
    index = 0
    for i in reply:
        activeplayers[index].redefine(i.posx,i.posy, i.rotation,i.id)
        index += 1
