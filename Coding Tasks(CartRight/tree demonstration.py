import pygame
# -- global constants
tree = [["A",-1,-1,0],
        ["B",0,2,0],
        ["D",-1,3,0],
        ["E",-1,-1,0],
        ["F",1,5,0],
        ["G",-1,6,0],
        ["I",-1,-1,0],
        ]

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
pygame.display.set_caption("Tree Demonstration")

# -- class definitions
class node(pygame.sprite.Sprite):
    def __init__(self,ref,x,y):
        super().__init__()
        self.image = pygame.Surface([32,32])
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #pygame.draw.circle(self.image, WHITE, (8, 8), 8)
        
        self.ref = ref
        self.name = tree[ref][0]
    def update(self):
        color = WHITE
        if (tree[self.ref][3] == 1):
            color = BLUE
        elif (tree[self.ref][3] == 2):
            color = YELLOW
        pygame.draw.circle(self.image, color, (16, 16), 16)

# -- Exit game flag set to false
done = False


all_sprites_list = pygame.sprite.Group()

A = node(0,80,150)
all_sprites_list.add(A)

B = node(1,160,100)
all_sprites_list.add(B)

D = node(2,240,150)
all_sprites_list.add(D)

E = node(3,320,200)
all_sprites_list.add(E)

F = node(4,320,50)
all_sprites_list.add(F)

G = node(5,480,100)
all_sprites_list.add(G)

I = node(6,560,150)
all_sprites_list.add(I)

def nodetick(currentnode):
    tree[currentnode][3] = 1

# -- Manages how fast the screen refreshes
clock = pygame.time.Clock()

### -- Game Loop
stack = []
stack.append(4)
treedone = False
currentnode = 4
tree[currentnode][3] = 1
stack.append(currentnode)
while not done:
    # -- user input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    

    # -- Game Logic goes after this comment
    if not treedone:
        tree[currentnode][3] = 1
        if (tree[currentnode][1] != -1) and (tree[(tree[currentnode][1])][3] != 2):
            currentnode = tree[currentnode][1]
            stack.append(currentnode)
        elif (tree[currentnode][2] != -1 and tree[(tree[currentnode][2])][3] != 2):
            currentnode = tree[currentnode][2]
            stack.append(currentnode)
        else:
            tree[currentnode][3] = 2
            if len(stack) != 0:
                currentnode = stack[len(stack)-1]
            else:
                currentnode = stack[1]
            stack.pop()
            print("ohno")
        if (currentnode == 4) and (tree[currentnode][3] == 2):
            treedone = True
            print("it done fucked up")

    # -- screen background is BLACK

    screen.fill(BLACK)

    # -- Draw here
    all_sprites_list.update()
    all_sprites_list.draw(screen)

    # -- flip display to reveal new position of objects
    pygame.display.flip()

    # - the clock ticks over
    clock.tick(5)

# - end of game loop

pygame.quit()
