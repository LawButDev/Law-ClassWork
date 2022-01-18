import pygame
import random
import math
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

size = (700, 500)
# Create the snow variables

class Snow():
    def __init__(self):
        self.x = random.randint(0,size[0])
        self.y = random.randint(0,size[1])
        self.size = random.randint(8,13)
        self.whitetone = (255-20*(13-self.size))
        self.surface = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.circle(self.surface,(self.whitetone,self.whitetone,self.whitetone), (self.size//2,self.size//2), self.size//2)
        self.mask = pygame.mask.from_surface(self.surface)
    def update(self):
        self.y += (1-((13-self.size)/8))
        self.x += math.sin(math.radians(self.y*(self.size-6)))
        if self.y >= size[1]:
            self.regen()
    def draw(self):
        self.whitetone = (255-20*(13-self.size))
        #pygame.draw.rect(self.surface,(self.whitetone,self.whitetone,self.whitetone), [0,0,self.size,self.size])
        pygame.draw.circle(self.surface,(self.whitetone,self.whitetone,self.whitetone), (self.size//2,self.size//2), self.size//2)
        screen.blit(self.surface,(self.x,self.y))
    def regen(self):
        self.y = -10
        self.x = random.randint(0,size[0])

class snowblocker():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.surface = pygame.Surface((size[0],size[1]),pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.surface)
    def update(self):
        for i in snowflakes:
            self.collision(i)
    def draw(self):
        screen.blit(self.surface,(0,0))
        self.mask = pygame.mask.from_surface(self.surface,250)
    def collision(self,snowdrop):
        if self.mask.overlap_area(snowdrop.mask,(int(snowdrop.x),int(snowdrop.y))) >= 20 and snowdrop.size > 10:
            snowdrop.regen()

class House(snowblocker):
    def __init__(self,x,y):
        super().__init__(x,y)
    def update(self):
        super().update()
    def draw(self):
        #pygame.draw.rect(self.surface,WHITE, [self.x-45,self.y-60,90,60])
        #pygame.draw.polygon(self.surface,WHITE,[(self.x-70,self.y-60),(self.x+70,self.y-60),(self.x,self.y-100)])
        pygame.draw.polygon(self.surface,WHITE,[(self.x+45,self.y),(self.x-45,self.y),(self.x-45,self.y-40),(self.x-70,self.y-40)
                                                ,(self.x,self.y-100),(self.x+70,self.y-40),(self.x+45,self.y-40)])
        pygame.draw.polygon(self.surface,WHITE,[(self.x+45,self.y-40),(self.x+45,self.y-80),(self.x+35,self.y-80),(self.x+35,self.y-40)])
        super().draw()
        
class Tree(snowblocker):
    def __init__(self,x,y,branches):
        super().__init__(x,y)
        self.branches = branches
    def update(self):
        super().update()
    def draw(self):
        pygame.draw.rect(self.surface,(200,200,200), [self.x-6,self.y-20,12,20])
        treeroot = 40
        for i in range(self.branches):
            self.drawbranch(self.y-(treeroot + 15*i),i)
        super().draw()
    def drawbranch(self,root,num):
        calccol = 255 - (10 * self.branches) + ((num + 1) * 10)
        col = (calccol,calccol,calccol)
        pygame.draw.polygon(self.surface,col,[(self.x-20,root+30),(self.x+20,root+30),(self.x,root)])

class lamppost(snowblocker):    
    def __init__(self,x,y,direction):
        super().__init__(x,y)
        self.direction = direction
        self.dircalc = -1 + 2*direction
    def update(self):
        super().update()
    def draw(self):
        self.surface.fill((0,0,0,0))
        pygame.draw.polygon(self.surface,WHITE,[(self.x - 4 * self.dircalc, self.y),(self.x-4*self.dircalc,self.y-10),(self.x-3*self.dircalc,self.y-10)
                                                ,(self.x - 3 * self.dircalc,self.y-80),(self.x + 3 * self.dircalc,self.y-80)
                                                ,(self.x + 3 * self.dircalc,self.y-70),(self.x + 25*self.dircalc,self.y-80),(self.x+40*self.dircalc,self.y-80)
                                                ,(self.x + 40 *self.dircalc,self.y-80),(self.x+50*self.dircalc,self.y-80),(self.x+50*self.dircalc,self.y-75)
                                                ,(self.x+40 * self.dircalc,self.y-75),(self.x+25*self.dircalc,self.y-75),(self.x+3*self.dircalc,self.y-65)
                                                ,(self.x+3 * self.dircalc,self.y-10),(self.x+4*self.dircalc,self.y-10),(self.x+3*self.dircalc,self.y)])
        #pygame.draw.rect(self.surface,WHITE, [self.x,self.y-80,8,80])
        #pygame.draw.rect(self.surface,WHITE, [self.x - (60*self.direction),self.y-80, 60,8])
        self.root = self.x - 45 + (90*self.direction)
        pygame.draw.polygon(self.surface,(255,255,255,150),[(self.root-20,self.y),(self.root+20,self.y),(self.root+2,self.y-74),(self.root-2,self.y-74)])
        super().draw()
        

snowflakes = []
for i in range(500):
    snowDrop = Snow()
    snowflakes.append(snowDrop)
snowflakes.sort(key = lambda flake: (flake.size))

furnishing = []

home = House(size[0]//2,size[1])
furnishing.append(home)
post = lamppost(size[0]//5,size[1],1)
furnishing.append(post)


tree = Tree(14*size[0]//20,size[1],3)
furnishing.append(tree)
tree = Tree(17*size[0]//20,size[1],4)
furnishing.append(tree)
tree = Tree(19*size[0]//20,size[1],3)
furnishing.append(tree)

pygame.init()
 
# Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Snow")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
    for snowdrop in snowflakes:
        snowdrop.update()
    for item in furnishing:
        item.update()
            
    # --- Screen-clearing code goes here
    screen.fill(BLACK)
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    
 
    # --- Drawing code should go here
    for snowdrop in snowflakes:
        snowdrop.draw()
    
    for item in furnishing:
        item.draw()
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(120)
 
# Close the window and quit.
pygame.quit()
