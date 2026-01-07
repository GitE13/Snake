import pygame,random,time,math
pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Roboto', 30)
grid_ds = (50,50)
allcells = [(i,j) for i in range(grid_ds[0]) for j in range(grid_ds[1])]
cellsize = 10
padding = 1
totalsize = cellsize + 2*padding
snakecells = [(grid_ds[0]//2-1,grid_ds[1]//2),(grid_ds[0]//2,grid_ds[1]//2),(grid_ds[0]//2+1,grid_ds[1]//2)]
hasbullets = 0
cooldown = 0
bullets = []
copfreeze = 0
for i in snakecells:
    allcells.remove(i)
text_surface = font.render(f'Score: {len(snakecells)}', True, (255, 255, 255))

direction = (1,0)
buttoninputs = pygame.K_UP
tick = 1
speed = 5
canvas = pygame.display.set_mode((grid_ds[0]*totalsize,grid_ds[1]*totalsize))
running = True
clock = pygame.time.Clock()

lastmove = direction

alive = True

visualq = []
speedq = []

class Apple:
    def __init__(self,color=[255,0,0]):
        if len(allcells) > 0:
            self.pos = random.choice(allcells)
            allcells.remove(self.pos)
        else:
            self.pos = [-100,-100]
        applelist.append(self)
        self.index = len(applelist)-1
        self.color = color
    def respawn(self):
        if len(allcells) > 0:
            self.pos = random.choice(allcells)
            allcells.remove(self.pos)
        else:
            self.pos = [-100,-100]
    def oneat(self):
        snakecells.insert(0,snakecells[0])
        self.respawn()

class Papple(Apple):
    def __init__(self, color=[212, 217, 119]):
        super().__init__(color)
    def oneat(self):
        if len(snakecells) == 1:
            deathanimation()
        else:
            everysnakecell.append(snakecells.pop(0))
            allcells.append(everysnakecell[-1])
        self.respawn()
        
class Vapple(Apple):
    def __init__(self, color=[255, 0, 255]):
        super().__init__(color)
    def oneat(self):
        super().oneat()
        for i in range(12*3):
            visualq.append(self.visualfunc)
    def visualfunc(self):
        clear = set([])
        for i in range(5):
            for j in range(5):
                clear.add((snakecells[-1][0]-2+i,snakecells[-1][1]-2+j))
        for i in path:
            if i not in clear:
                color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                pygame.draw.rect(canvas,color,(i[0]*totalsize,i[1]*totalsize,cellsize,cellsize))
                
class Flashapple(Vapple):
    def __init__(self, color=[100, 100, 100]):
        super().__init__(color)
    def visualfunc(self):
        color = (tick%2) * 255
        color = [color,color,color]
        for i in path:
            pygame.draw.rect(canvas,color,(i[0]*totalsize,i[1]*totalsize,cellsize,cellsize))
            
class Sapple(Apple):
    def __init__(self, color=[173, 216, 230]):
        super().__init__(color)
    def oneat(self):
        super().oneat()
        speedq.append([1,60*5])
class Mapple(Apple):
    def __init__(self, color=[0, 100, 0]):
        super().__init__(color)
    def oneat(self):
        super().oneat()
        speedq.append([10,60*5])
class Tapple(Apple):
    def __init__(self, color=[255, 0,50]):
        super().__init__(color)
    def oneat(self):
        super().oneat()
        canvas.fill([0,0,0])
        pygame.display.flip()
        time.sleep(10)
        if len(snakecells) == 2:
            deathanimation()
        else:
            everysnakecell.append(snakecells.pop(0))
            everysnakecell.append(snakecells.pop(0))
            allcells.append(everysnakecell[-1])
            allcells.append(everysnakecell[-2])
class Bapple(Apple):
    def __init__(self, color=[192, 192, 192]):
        super().__init__(color)
    def oneat(self):
        global hasbullets
        super().oneat()
        hasbullets += 3 #Custom How much ammo a bullet gives
        

applelist:list[Apple] = []
        

apples = [Apple() for i in range(5)]

papples = [Papple() for i in range(1)]
vapples = [Vapple() for i in range(1)]
fapples = [Flashapple() for i in range(1)]
sapples = [Sapple() for i in range(1)]
mapples = [Mapple() for i in range(1)]
tapples = [Tapple() for i in range(1)]
bapples = [Bapple() for i in range(5)]

#Custom Each of those numbers is how many of that apple you want



def init():
    global snakecells,direction,buttoninputs,tick,lastmove,alive,ticksfromapple,applelist,visualq,speedq,copcells,everysnakecell,allcells,cooldown,hasbullets,bullets,copfreeze
    visualq = []
    speedq = []
    allcells = [(i,j) for i in range(grid_ds[0]) for j in range(grid_ds[1])]
    
    snakecells = [(grid_ds[0]//2-1,grid_ds[1]//2),(grid_ds[0]//2,grid_ds[1]//2),(grid_ds[0]//2+1,grid_ds[1]//2)]
    for i in snakecells:
        allcells.remove(i)
    for i in applelist:
        i.respawn()
    direction = (1,0)
    buttoninputs = pygame.K_UP
    tick = 1
    lastmove = direction
    alive = True
    ticksfromapple = 1
    cooldown = 0
    hasbullets = 0
    copfreeze = 0
    copcells = []
    everysnakecell = []
    bullets = []


def changedirectionofsnake(buttoninput):
    global direction,lastmove
    if (buttoninput == pygame.K_UP or buttoninput == pygame.K_w) and lastmove != (0,1):
        direction = (0,-1)
        
    elif (buttoninput == pygame.K_DOWN or buttoninput == pygame.K_s) and lastmove != (0,-1):
        direction = (0,1)
        
    elif (buttoninput == pygame.K_LEFT or buttoninput == pygame.K_a) and lastmove != (1,0):
        direction = (-1,0)
        
    elif (buttoninput == pygame.K_RIGHT or buttoninput == pygame.K_d) and lastmove != (-1,0):
        direction = (1,0)

def movesnake():
    global lastmove,apple,papple,ticksfromapple
    snakecells.append((snakecells[-1][0]+direction[0],snakecells[-1][1]+direction[1]))
    lastmove = direction
    for applei in applelist:
        if applei.pos == snakecells[-1]:
            applei.oneat()
            ticksfromapple = 1
    allcells.append(snakecells.pop(0))
    global text_surface
    text_surface = font.render(f'Score: {len(snakecells)}', True, (255, 255, 255))
      
def drawsnake():      
    for cell in snakecells[1:]:
        pygame.draw.rect(canvas,[0,255,0],(cell[0]*totalsize,cell[1]*totalsize,cellsize,cellsize))
    left = (60*5) - ticksfromapple
    left /= (60*5)
    newcellsize = cellsize * left
    takencellsize = cellsize-newcellsize
    pygame.draw.rect(canvas,[0,255,0],(snakecells[0][0]*totalsize+takencellsize/2,snakecells[0][1]*totalsize+takencellsize/2,newcellsize,newcellsize))
def drawcop():      
    for cell in copcells:
        pygame.draw.rect(canvas,[0,0,255],(cell[0]*totalsize-totalsize,cell[1]*totalsize,cellsize,cellsize))
    
def drawscreen(snake=True):
    canvas.fill([0,0,0])
    
    for applei in applelist:
        pygame.draw.rect(canvas,applei.color,(applei.pos[0]*totalsize,applei.pos[1]*totalsize,cellsize,cellsize))
    if snake:
        drawsnake()
    drawcop()
        
    if len(visualq) > 0:
        visual = visualq.pop(0)
        visual()
        
    canvas.blit(text_surface,(canvas.get_width()-text_surface.get_width()-10,10))
    ammo = font.render(f'Ammo: {hasbullets}', True, (255, 255, 255))
    canvas.blit(ammo,(canvas.get_width()-ammo.get_width()-10,10+text_surface.get_height()))
    
    for i in bullets:
        pygame.draw.circle(canvas,[192,192,192],i[0],5)
        
    pygame.display.flip()

    
def checkdeath():
    if snakecells[-1] in snakecells[:-1]:
        return True
    if (snakecells[-1][0]+1)%(grid_ds[0]+1) == 0 or (snakecells[-1][1]+1)%(grid_ds[1]+1) == 0:
        return True
    return False

def deathanimation():
    alive = False
    for i in range(5):
        drawscreen()
        pygame.display.flip()
        clock.tick(10)
        drawscreen(False)
        clock.tick(10)
    canvas.fill([0,0,0])
    pygame.display.flip()
    clock.tick(1)
    init()


def createpathbase():
    path = [(0,0)]
    for i in range(grid_ds[1]//2):
        for j in range(grid_ds[1]-1):
            path.append((j+1,i*2))
        for j in range(grid_ds[1]-1,0,-1):
            path.append((j,i*2+1))
    for i in range(grid_ds[1]-1,0,-1):
        path.append((0,i))
    return(path)

path = createpathbase()

def drawpathcolors():
    colormulti = 255/len(path)
    for i in range(len(path)):
        pygame.draw.rect(canvas,[i*colormulti,i*colormulti,i*colormulti],(path[i][0]*totalsize,path[i][1]*totalsize,cellsize,cellsize)) # type: ignore
def followai(follow=True):
    if follow:
        pathindex = path.index(snakecells[-1])+1
        pathtile = path[pathindex%len(path)]
        global direction
        direction = (pathtile[0]-snakecells[-1][0],pathtile[1]-snakecells[-1][1])
    movesnake()
    
def sign(n):
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1
    
def shoot():
    snakeloc = (snakecells[-1][0]*totalsize+totalsize/2,snakecells[-1][1]*totalsize+totalsize/2)
    mousepos = pygame.mouse.get_pos()
    move = (mousepos[0]-snakeloc[0],mousepos[1]-snakeloc[1])
    movel = math.sqrt(move[0]**2+move[1]**2)
    bullets.append([snakeloc,(move[0]/movel*600,move[1]/movel*600)])
def getdistance(p1,p2):
    move = (p1[0]-p2[0],p1[1]-p2[1])
    return math.sqrt(move[0]**2+move[1]**2)
def updatebullets():
    global copfreeze
    for i in bullets:
        i[0] = (i[0][0]+i[1][0]/60,i[0][1]+i[1][1]/60)
        for cell in copcells:
            cellpos = (cell[0]*totalsize+totalsize/2,cell[1]*totalsize+totalsize/2)
            d = (i[0][0]-cellpos[0],i[0][1]-cellpos[1])
            distance =  math.sqrt(d[0]**2+d[1]**2)
            if distance < totalsize*2:
                copfreeze = 300 #Custom How long the cop stops when you hit him
            elif distance < totalsize*2 * 5: #Custom That second number is how much bigger his 'nearby' area is
                copfreeze = 20 #Custom How long the cop stops when you almost hit him
    
copcells = []
everysnakecell = []
createpathbase()
ticksfromapple = 1
if __name__ == '__main__':
    init()
    drawscreen()
    snakesave = snakecells.copy()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                changedirectionofsnake(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hasbullets > 0 and cooldown <= 0:
                    cooldown = 30
                    hasbullets -= 1
                    shoot()
        if alive:
            if tick % speed == 0:
                snakesave = snakecells.copy()
                followai(False)
                everysnakecell.append(snakecells[0])
                if tick > 20:
                    if copfreeze <= 0:
                        if len(set(copcells)) < 1:
                            copcells.append(everysnakecell.pop(0))
                        elif random.random() < .7:
                            cophead = copcells[-1]
                            snakehead = snakecells[-1]
                            diff = [snakehead[0]-cophead[0],snakehead[1]-cophead[1]]
                            if 0 not in diff:
                                number = random.randint(0,1)
                                diff[number] = 0
                            newhead = (cophead[0] + sign(diff[0]),cophead[1] + sign(diff[1]))
                            copcells.append(newhead)
                            allcells.append(copcells.pop(0))
                            if sum([abs(snakehead[0]-cophead[0]),abs(snakehead[1]-cophead[1])]) <= 1:
                                deathanimation()
        updatebullets()
        drawscreen()
        if alive == checkdeath():
            snakecells = snakesave
            deathanimation()
        clock.tick(60)
        if ticksfromapple % (60*5) == 0:
            ticksfromapple = 1
            if len(snakecells) == 1:
                deathanimation()
            else:
                everysnakecell.append(snakecells.pop(0))
                allcells.append(everysnakecell[-1])
        tick += 1
        cooldown -= 1
        ticksfromapple += 1
        copfreeze -= 1
        if len(speedq) > 0:
            if speedq[0][1] > 0:
                speed = speedq[0][0]
                speedq[0][1] -= 1
            else:
                speed = speedq[0][0]
                speedq.pop(0)
        else:
            speed = 5


# Search for 'Custom' for all the values you can customize
