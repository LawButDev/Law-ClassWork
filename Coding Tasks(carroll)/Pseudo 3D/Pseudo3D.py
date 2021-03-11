import pygame
import math
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
planewidth = 320
walldist = []
res = 3
raylength = 10

for f in range(planewidth):
    tempgridthing = [100000,10000,10000]
    walldist.append(tempgridthing)
    

projdist = int((planewidth // 2) / math.tan((30 * math.pi / 180 )))
rayang = 60 / 320
# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)

# -- initialise PyGame
pygame.init()

# -- Blank Screen
size = (640,640)
screen = pygame.display.set_mode(size)

# -- Title of new window/screen
pygame.display.set_caption("Psuedo 3D")


# -- class list definitions
debug_list = pygame.sprite.Group()
debug_wallcol = pygame.sprite.Group()

# -- sprite loading
fwall=pygame.image.load('factory-wall.png').convert()
fwallcomp = pygame.image.load('factory-wall-disp.png').convert()

# -- class definitions
class debugsquare(pygame.sprite.Sprite):
    def __init__(self,x_ref,y_ref):
        super().__init__()
        #self.image = pygame.Surface([size[0] // 20,size[1] // 20],pygame.SRCALPHA)
        self.image = pygame.Surface((unit,unit),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.y = y_ref
        self.rect.x = x_ref
        self.selected = False
        self.sprite = fwall
    def update(self):
        if self.selected:
            self.image.fill((30,150,255,100))
        else:
            self.image.fill((255,255,255,100))        
        self.selected = False

class player(pygame.sprite.Sprite):
    def __init__(self,x_ref,y_ref):
        super().__init__()
        self.image = pygame.Surface([size[0] // 20,size[1] // 20],pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        #self.image.fill((150,150,200,100))
        pygame.draw.polygon(self.image, (150,150,200,100), ((self.rect.center[0],self.rect.top),(self.rect.left,self.rect.bottom),(self.rect.right,self.rect.bottom)))           
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
        self.image = pygame.transform.rotate(self.orgimage, -self.rot - 90)
        self.dirx = 0
        self.diry = 0
        
        #floor render
        pygame.draw.rect(screen,(100,100,100,255),(0,size[1]//2,size[0], size[1] // 2),0)

        #ceilling render
        pygame.draw.rect(screen,(0,0,100,255),(0,0,size[0], size[1] // 2),0)

        for f in range(planewidth):
            i = (f*rayang) + self.rot - 30
            if (i <= 0): i += 360
            if (i > 360): i -= 360
            hypot = raylength * unit
            xdif = math.cos(math.radians(i)) * hypot
            ydif = math.sin(math.radians(i)) * hypot
            mindis = 100000
            colx = xdif + self.rect.center[0]
            coly = ydif + self.rect.center[1]

            sprite = fwall
            corsprite = fwall
            
            for col in debug_wallcol:
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

            #wall height calc based on distance to proj plane (projdist)
            projheight = (64 / cordist) * projdist

            #debug basic render of view using lines (needs to be rewritten to sprite) - since the porj plane must be doubled in size the height is doubled and x coord is doubled
            #distance colour change is to make it easier to see depth, by making it darker
            dcc = max((255-((cordist)//3)**1), 10)

            #in order to get an image rendering properly, it must first be scaled, then a one pixel wide slice of the sprite must be displayed
            dispsprite = pygame.transform.scale(corsprite,(2,int(projheight)*2))
            cont_rect = pygame.Rect((0,0),(2, int(projheight)*2))

            screen.blit(dispsprite,(2*f,1*(size[1]//2-projheight//1)),cont_rect)

            #adds an overlay of darkness to amke depth easier to make out
            overlayline = pygame.Surface((2,int(projheight * 2)),pygame.SRCALPHA)
            overlayline.fill((0,0,0,255-dcc))
            screen.blit(overlayline,(2*f,1*(size[1]//2-projheight//1)))
            
            #pygame.draw.line(screen,(dcc // 6,dcc//3,dcc // 1,175),(2*f,1*(size[1]//2 - projheight // 1)),(2*f,1*(size[1]//2 + projheight // 1)),2)
            
####            #debug rendering of view cone - should be disabled once done
####            pygame.draw.line(screen, (255,255,10,0), (self.rect.center),(colx, coly),1)

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
        
        self.rect.x += self.xdif

        #for foo in player_collide_list:
        #    self.rect.x = oldx
##
##    
##            if (pygame.Rect(self.rect.x + self.xdif + 1,self.rect.y,  # +1
##                                self.rect.width, self.rect.height)
##                    .colliderect(foo.rect) and self.rect.x + self.xdif // 2 <= foo.rect.x and self.dirx == -1):
##                self.rect.right = foo.rect.left
##            elif (pygame.Rect(self.rect.x + (self.xdif - 1),self.rect.y,  # +1
##                                self.rect.width, self.rect.height)
##                    .colliderect(foo.rect) and self.rect.x + self.xdif // 2 >= foo.rect.x and self.dirx == 1):
##                self.rect.left = foo.rect.right

        
        oldy = self.rect.y
        
        self.rect.y += self.ydif

        player_collide_list = pygame.sprite.spritecollide(self, debug_wallcol, False)

        for foo in player_collide_list:
            self.rect.y = oldy
            self.rect.x = oldx
            #if self.rect.bottom < foo.rect.top:
            #    self.rect.y = oldy 
            #elif self.rect.top > foo.rect.bottom:
            #    self.rect.y = oldy 


for y in range (mapsizey):
    ystr = map.readline()
    for x in range (mapsizex):
        if ystr[x] == "#":
            test = debugsquare(int(y)*unit,int(x) * unit)
            debug_list.add(test)
            debug_wallcol.add(test)
            test.sprite = fwall
        if ystr[x] == "c":
            test = debugsquare(int(y)*unit,int(x) * unit)
            debug_list.add(test)
            debug_wallcol.add(test)
            test.sprite = fwallcomp


PC = player(size[1]//2 + 30, size[0]//2 + 30)
debug_list.add(PC)
        
# -- Exit game flag set to false
done = False

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

#test = debugsquare(300,300)
#debug_list.add(test)

### -- Game Loop

while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()
    #if keys[pygame.K_LEFT]:
        #test.selected = True
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
