import pygame
import math
import socket
from network import Network
# -- global constants
map = open("map.txt","r")

mapsizex = 11
mapsizey= 7
savedmap = []
for line in range(mapsizey):
    savedmap.append(map.readline())
map.seek(0)
unit = 64
pmm = 1/16
mossen = -0.25
planewidth = 540
walldist = []
res = 3
raylength = 10
debugmode = False

rawspawnpoint = ""
rawmapsize = ()

Playername = "pogman"
clientnumber = 0

for f in range(planewidth):
    tempgridthing = [100000,10000,10000]
    walldist.append(tempgridthing)
    

projdist = int((planewidth // 2) / math.tan((30 * math.pi / 180 )))
rayang = 60 / planewidth
# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (1080,640)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Psuedo 3D")


# -- class list definitions
debug_list = pygame.sprite.Group()
debug_wallcol = pygame.sprite.Group()
debug_entlist = pygame.sprite.Group()
debug_raycol = pygame.sprite.Group()
debug_bullet = pygame.sprite.Group()
debug_masked = pygame.sprite.Group()

# -- sprite loading
fwall=pygame.image.load('factory-wall.png').convert()
fwallcomp = pygame.image.load('factory-wall-disp.png').convert()

#multi face sprites should be in the standard form front, right, back, left, to make renderring easier
arrow = (pygame.image.load('arrowf.png'),pygame.image.load('arrowr.png'),pygame.image.load('arrowb.png'),pygame.image.load('arrowl.png'))

sp = pygame.image.load('spawnpost.png')
bulspr = pygame.image.load('shitbullet.png')

# -- subroutine definitions

### - only used once so not put in a class, handles the initial unpacking of the map and 
def initialunpack(strog):
    global rawmapsize
    global rawspawnpoint
    global rawmap
    strog = strog.split("/")
    rawmapsize = strog[0]
    rawspawnpoint = strog[1]
    rawmap = strog [2]
    rawmapsize = rawmapsize.split(" ")
    rawmapsize = (int(rawmapsize[0]),int(rawmapsize[1]))


# - corrects an angle to be back into the desired 0-360 range
def anglecor(ang):
    if ang <= 0:
        return(ang + 360)
    elif ang > 360:
        return(ang - 360)
    else:
        return(ang)



# -- class definitions

# - networking class - deprecated because i moved it to a separate file
                             

## -- map + sprite renderring classes
class debugsquare(pygame.sprite.Sprite):
    def __init__(self,x_ref,y_ref):
        super().__init__()
        self.type = "block"
        self.image = pygame.Surface((unit,unit),pygame.SRCALPHA)
        self.image.fill((100,200,100,255))
        self.rect = self.image.get_rect()
        self.rect.y = y_ref
        self.rect.x = x_ref
        self.selected = False
        self.sprite = fwall

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
    def  update(self):
        self.spritecentdist = math.sqrt((abs(PC.rect.center[0]-self.rect.center[0]))**2 + (abs(PC.rect.center[1]-self.rect.center[1]))**2)
        self.spritecentang = math.degrees((math.atan2((PC.rect.center[1]-self.rect.center[1]),(PC.rect.center[0]-self.rect.center[0])))%(2*math.pi))
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

class rotent(ent):
    def __init__(self,x_ref,y_ref,x_size,y_size,sprites,rot):
        super().__init__(x_ref,y_ref,x_size,y_size,sprites[0])
        self.rot = rot
        self.sprites = sprites
    def update(self):
        super().update()
        self.relativerot = self.rot - math.degrees((math.atan2((self.rect.center[1]-PC.rect.center[1]),(self.rect.center[0]-PC.rect.center[0])))%(2*math.pi))
        #adjustment to make calcs easier
        self.relativerot -= 45
        if self.relativerot <= 0 : self.relativerot += 360
        elif self.relativerot > 360: self.relativerot -= 360

        if (self.relativerot >= 0) and (self.relativerot < 90):
            self.sprite = self.sprites[2]
        elif (self.relativerot >= 90) and (self.relativerot < 180):
            self.sprite = self.sprites[1]
        elif (self.relativerot >= 180) and (self.relativerot < 270):
            self.sprite = self.sprites[0]
        elif (self.relativerot >= 270) and (self.relativerot < 360):
            self.sprite = self.sprites[3]

class enemy(rotent):
    def __init__(self,x_ref,y_ref,x_size,y_size,sprites,rot,player):
        super().__init__(self,x_ref,y_ref,x_size,y_size,sprites,rot)
        self.player = player
    def update(self):
        super().update()

class bullet(ent):
    def __init__(self,x_ref,y_ref,x_size,sprite,owner,damage,bmm,ang):
        super().__init__(x_ref + 1,y_ref + 1,x_size,64,sprite)
        self.owner = owner
        self.damage = damage
        self.bmm = bmm
        self.ang = ang
        super().update()
    def update(self):
        super().update()
        self.x_move = math.cos(math.radians(self.ang)) * (unit * self.bmm)
        self.y_move = math.sin(math.radians(self.ang)) * (unit * self.bmm)
        self.rect.center = (self.rect.center[0] + self.x_move,self.rect.center[1] + self.y_move)
        bullet_collide_list = pygame.sprite.spritecollide(self, debug_wallcol, False)
        for foo in bullet_collide_list:
            self.kill()

## -- weaponry classes

class gun(pygame.sprite.Sprite):
    def __init__(self,sprite,damage,bulletspr,bmm,firerate):
        super().__init__()
        self.image = pygame.Surface((1,1),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.sprite = sprite
        self.damage = damage
        self.bulspr = bulletspr
        self.bmm = bmm
        self.firerate = firerate
        self.shooting = False
        self.lastshot = pygame.time.get_ticks()
    def update(self):
        ev = pygame.event.get()
        for event in ev:
            #mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
              self.shooting = True
            #mouse up
            elif event.type == pygame.MOUSEBUTTONUP:
              self.shooting = False
        if self.shooting:
            tick = pygame.time.get_ticks()
            if self.lastshot <= tick:
                self.lastshot = tick + self.firerate
                bul = bullet(PC.rect.center[0],PC.rect.center[1],8,self.bulspr,Playername,self.damage,self.bmm,PC.rot)
                debug_list.add(bul)
                debug_entlist.add(bul)
                debug_raycol.add(bul)
                debug_bullet.add(bul)

class pistol(gun):
    def __init__(self):
        super().__init__(bulspr,10,bulspr,1/2,500)
    def update(self):
        super().update()
                
            
        

## -- player character and enemy classes - npcs and shit

class player(pygame.sprite.Sprite):
    def __init__(self,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([int(unit * 3/4),int(unit * 3/4)],pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        #self.image.fill((150,150,200,100))
        #pygame.draw.polygon(self.image, (150,150,200,100), ((self.rect.center[0],self.rect.top),(self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom)))           
        pygame.draw.circle(self.image, (150,150,200,250), (self.rect.center), int(unit * 3/4) // 2,0)
        self.rect.y = y_ref
        self.rect.x = x_ref
        self.dirx = 0
        self.diry = 0
        self.fov = 60
        self.rot = 0
        self.orgimage = self.image
    def update(self):
        #ay_angle=view_angle+(half_fov);ray_look=view_look+int(half_fov*ratio)
        for f in range(planewidth):
            walldist[f][0] = 10000
            walldist[f][1] = 10000
            walldist[f][2] = 10000
        pygame.event.set_grab(True) 
        pygame.mouse.set_visible(False)
        delta_y, delta_x = pygame.mouse.get_rel()
        #pygame.mouse.set_pos([size[1] // 2, size[0] // 2])
        self.rot += float(-delta_y * mossen)
        while self.rot > 360:
            self.rot = self.rot - 360
        while self.rot < 0:
            self.rot = self.rot + 360
        #self.rotation_direction.y = float(delta_y)
        #self.image = pygame.transform.rotate(self.orgimage, -self.rot - 90)
        self.dirx = 0
        self.diry = 0

        if not(debugmode):
            
            #floor render
            pygame.draw.rect(screen,(100,100,100,255),(0,size[1]//2,size[0], size[1] // 2),0)

            #ceilling render
            pygame.draw.rect(screen,(0,0,100,255),(0,0,size[0], size[1] // 2),0)

        else:
            debug_raycol.draw(screen)

        # to attempt to solve the lag caused by checking every object for every ray every frame im attempting to use a mask to only check the blocks that are in the players fov
        masksurf = pygame.Surface([mapsizex*unit,mapsizey*unit],pygame.SRCALPHA)
        maskrect = masksurf.get_rect()
        #draws a triangle represent the viewcone        
        hypot = raylength * unit * 1
        calcrot = anglecor(self.rot - 30)
        xdif = math.cos(math.radians(calcrot)) * hypot
        ydif = math.sin(math.radians(calcrot)) * hypot
        calcrot = anglecor(self.rot + 30)
        xdif2 = math.cos(math.radians(calcrot)) * hypot
        ydif2 = math.sin(math.radians(calcrot)) * hypot
        
        pygame.draw.polygon(masksurf, (100,0,0,200), [(self.rect.center[0], self.rect.center[1]),(self.rect.center[0] + xdif, self.rect.center[1] + ydif),(self.rect.center[0] + xdif2, self.rect.center[1] + ydif2)],0)

        viewMask = pygame.mask.from_surface(masksurf)
        
        debug_masked.empty()
        
        for col in debug_raycol:
          #  if (pygame.sprite.collide_mask(self, col) != None): ### --- its not running because this check is failing, meaning the culled mask isn't working
            if not(viewMask.overlap(pygame.mask.from_surface(col.image),(col.rect.x,col.rect.y)) is None):
                debug_masked.add(col)
            #screen.blit(pygame.mask.from_surface(col.image).to_surface(),(col.rect.x,col.rect.y))
                
        
        for f in range(planewidth):
            i = anglecor((f*rayang) + self.rot - 30)
            hypot = raylength * unit
            xdif = math.cos(math.radians(i)) * hypot
            ydif = math.sin(math.radians(i)) * hypot
            mindis = 100000
            colx = xdif + self.rect.center[0]
            coly = ydif + self.rect.center[1]

            sprite = fwall
            corsprite = fwall
            spritecorsprite = fwall

            spritedist = 100000000000
            spritecolx = xdif + self.rect.center[0]
            spritecoly = ydif + self.rect.center[1]
            
            for col in debug_masked:
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
                        if dist < spritedist: # and dist < col.x_size:
                            spritedist = dist
                            sprite = col.sprite
                            spriteloc = 0

                            #concept of new sprite render is to find the length of the line between the ray and the centre of the sprite, and if it is within the sprite boudnary working from there
                            #this line finds the distance between the angles for later calculation
                            angdif = abs(i - col.spritecentang) % 360
                            #since the difference can be maximum 1
                            if angdif >= 180 : angdif = 360 - angdif
                            #relspritedist = ((math.tan(math.radians(abs(i % 90 - col.spritecentang%90)))*col.spritecentdist))
                            relspritedist = abs((math.tan(math.radians(abs(angdif)))*col.spritecentdist))
                            if relspritedist < 0: relspritedist = 0
                            if relspritedist <= col.x_size // 2:
                                #if (i%90 <= col.spritecentang%90):
                                if col.angcompare(i,col.spritecentang):  
                                    spriteloc = int(col.x_size//2 - relspritedist) 
                                #elif (i%90 > col.spritecentang%90):
                                else:
                                    spriteloc = int(col.x_size//2 + relspritedist) 
                            else:
                                sprite = sp
                                
                            spritedist = col.spritecentdist
    
                            spritecorsprite = pygame.Surface.subsurface(sprite, (spriteloc, 0, 1, 64))
                            
                if col.type == "block":
                    clippedline = col.rect.clipline((self.rect.center[0],self.rect.center[1]),(self.rect.center[0] + xdif , self.rect.center[1] + ydif))
                    if clippedline:
                        start,end = clippedline
                        #pygame.draw.line(screen, (255,255,10,175), (start),(end),2)
                        dist = math.sqrt((abs(self.rect.center[0]-start[0]))**2 + (self.rect.center[1]-start[1])**2)
                        if dist < mindis:
                            colx = start[0]
                            coly = start[1]
                            mindis = dist
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
                        
            #angle correction to reduce distortion
            corang = f*rayang - 30
            dist = math.sqrt((abs(self.rect.center[0]-colx))**2 + (self.rect.center[1]-coly)**2)
            cordist = math.cos(math.radians(corang))*dist
            if cordist == 0: cordist += 0.000001

            spritecordist = spritedist
            spritecordist = math.cos(math.radians(corang))* spritedist
            if spritecordist == 0: spritecordist += 0.000001

            #wall height calc based on distance to proj plane (projdist)
            projheight = (unit / cordist) * projdist
            if projheight >= size[1]: projheight = size [1]

            #sprite height calc based on distance to proj plane(porjdist)
            spriteprojheight = (unit/spritecordist)*projdist
            if spriteprojheight >= size[1] : spriteprojdist = size[1]

            #debug basic render of view using lines (needs to be rewritten to sprite) - since the porj plane must be doubled in size the height is doubled and x coord is doubled
            #distance colour change is to make it easier to see depth, by making it darker
            dcc = max((255-((cordist)//3)**1), 10)

            #in order to get an image rendering properly, it must first be scaled, then a one pixel wide slice of the sprite must be displayed
            dispsprite = pygame.transform.scale(corsprite,(2,int(projheight)*2))
            cont_rect = pygame.Rect((0,0),(2, int(projheight)*2))

            spritedispsprite = pygame.transform.scale(spritecorsprite,(2,int(spriteprojheight)*2))
            spritecont_rect = pygame.Rect((0,0),(2, int(spriteprojheight)*2))
            
            if not(debugmode):
                screen.blit(dispsprite,(2*f,1*(size[1]//2-projheight//1)),cont_rect)

            #adds an overlay of darkness to amke depth easier to make out
            overlayline = pygame.Surface((2,int(projheight * 2)),pygame.SRCALPHA)
            overlayline.fill((0,0,0,255-dcc))
            screen.blit(overlayline,(2*f,1*(size[1]//2-projheight//1)))
            if spritedist < cordist:
                screen.blit(spritedispsprite,(2*f,1*(size[1]//2-spriteprojheight//1)),spritecont_rect)

            
            #pygame.draw.line(screen,(dcc // 6,dcc//3,dcc // 1,175),(2*f,1*(size[1]//2 - projheight // 1)),(2*f,1*(size[1]//2 + projheight // 1)),2)
                

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

        #player_collide_list = pygame.sprite.spritecollide(self, debug_wallcol, False)

        oldx = self.rect.x
        
        #self.rect.x += self.xdif
        
        oldy = self.rect.y

        coll_group = pygame.sprite.Group()
        coll_group.empty()
        
        #self.rect.y += self.ydif
        for foo in debug_wallcol:
            if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(foo.image),(int((self.rect.x + self.xdif) - foo.rect.x),int((self.rect.y + self.ydif) - foo.rect.y))) is not None:
                coll_group.add(foo)
        if len(coll_group) != 0:
            xcolld = False
            ycolld = False
            for foo in coll_group:
                if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(foo.image),(int((self.rect.x + self.xdif) - foo.rect.x),int((self.rect.y) - foo.rect.y))) is not None:
                    xcolld = True
                if pygame.mask.from_surface(self.image).overlap(pygame.mask.from_surface(foo.image),(int((self.rect.x) - foo.rect.x),int((self.rect.y + self.ydif) - foo.rect.y))) is not None:
                    ycolld = True
            if not xcolld:
                self.rect.x += self.xdif
            if not ycolld:
                self.rect.y += self.ydif
        else:
            self.rect.x += self.xdif
            self.rect.y += self.ydif
            
        player_collide_list = pygame.sprite.spritecollide(self, debug_wallcol, False)

        for foo in player_collide_list:
            if self.rect.x <= foo.rect.x:
                if self.rect.right > foo.rect.left:
                    self.rect.x -= 1
            else:
                if self.rect.left < foo.rect.right:
                    self.rect.x += 1
            #self.rect.y = oldy
            if self.rect.y <= foo.rect.y:
                if self.rect.bottom > foo.rect.top:
                    self.rect.y += 1
            else:
                if self.rect.top < foo.rect.bottom:
                    self.rect.y -= 1

            #self.rect.x = oldx


gotip = False
while not gotip:
    print("please enter the ip of the server in form ##.#.#.##")
    ip = input()
    gotip = True
    interface = Network(ip)
    initialunpack(interface.id)


mapsizex = int(rawmapsize[0])
mapsizey = int(rawmapsize[1])

print(mapsizex,mapsizey)

#print(rawspawnpoint)
spawnpoint = rawspawnpoint.split(" ")
PC = player(unit * int(spawnpoint[1]), unit*int(spawnpoint[0]))
debug_list.add(PC)

map = rawmap.split("\n")
for y in range (mapsizey):
    ystr = map[y]
    for x in range (mapsizex):
        if ystr[x] == "#":
            test = debugsquare(int(y)*unit,int(x) * unit)
            debug_list.add(test)
            debug_wallcol.add(test)
            test.sprite = fwall
            debug_raycol.add(test)
        if ystr[x] == "c":
            test = debugsquare(int(y)*unit,int(x) * unit)
            debug_list.add(test)
            debug_wallcol.add(test)
            test.sprite = fwallcomp
            debug_raycol.add(test)
        if ystr[x] == "s":
            spawnpoint = ent(int(y*unit) + unit//2, int(x*unit) + unit//2, unit//2,unit//2, sp)
            debug_list.add(spawnpoint)
            debug_raycol.add(spawnpoint)





gun = pistol()
debug_list.add(gun)
        
        
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
