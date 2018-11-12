import random
sz=10
speed=30
grid=[ [0]*sz for _ in range (sz)]
w=600/sz

# -2: Destino
# -1: Avatar
# 0: Fondo
# 1-5: Obstaculo

# (x,y) personaje
avax=0
avay=0

#(x,y) premio
trex=(sz-1)
trey=(sz-1)

#boton1
b1x=650
b1y=55
b1w=100
b1h=20

#boton2
b2x=620
b2y=100
b2w=70
b2h=70

#boton3
b3x=700
b3y=100
b3w=70
b3h=70

#bar
barx=690
bary=225
barw=20
barh=200

#lever
levx=barx-5
levy=bary + barh
levw=30
levh=20
overLever=False
locked=False
yOffset=0.0

#PercentLever
perx=barx
pery=bary-5
percent=0.0

#Buttonobstacules
b4x=610
b4y=555
b4w=200
b4h=20

#List of (x,y)
global bresenList, lastBox
iterBresen=0

def setup():
  size(820,600)
  global play,puttingAvatar, puttingPremio,bresenList,lastBox,doBresen,played
  global grassImg,avatarImg,premioImg,obs1,obs2,obs3,obs4,obs5
  avatarImg=loadImage("gatitu.png")
  grassImg=loadImage("pixil-frame-0.png")
  premioImg=loadImage("castillito.png")
  obs1=loadImage("fueguito.png")
  obs2=loadImage("fueguito.png")
  obs3=loadImage("fueguito.png")
  obs4=loadImage("fueguito.png")
  obs5=loadImage("fueguito.png")
  play=False
  puttingAvatar=False
  puttingPremio=False
  bresenList=[]
  lastBox=Stack()
  iterBresen=0
  doBresen=True
  played=False
  
def draw():
    if play:
        findWay()
        delay(speed)
    interface()

def findWay():
    global avax,avay,lastBox,play,iterBresen, doBresen, grid, played
    options=[]
    if avax==trex and avay==trey:
        endWin()
        return
    if doBresen:
        bresenham(avax,avay,trex,trey)
    print "actual: "+str(avax)+" "+str(avay)
    if len(bresenList)>1 and grid[bresenList[iterBresen][0]][bresenList[iterBresen][1]]<5:
        lastBox.push((avax,avay))
        avax=bresenList[iterBresen][0]
        avay=bresenList[iterBresen][1]
        if(avax==trex and avay==trey):
            endWin()
            return
        iterBresen+=1
        doBresen=False
        return
    else: grid[avax][avay]+=1
    doBresen=True
    cont=0
    for x in range(-1,2):
        for y in range(-1,2):
            if avax+x>=0 and avax+x<=sz-1 and avay+y>=0 and avay+y<=sz-1:
                if lastBox.size()>0 and grid[avax+x][avay+y]<5 and (avax+x,avay+y)!=lastBox.peek() and not (x==0 and y==0) :
                    cont+=1
                    options.append((x,y))
                elif lastBox.isEmpty() and grid[avax+x][avay+y]<5 and not (x==0 and y==0):
                    cont+=1
                    options.append((x,y))
    if cont==0 and lastBox.size>0:
        elem=lastBox.peek()
        if grid[elem[0]][elem[1]]<5:
            grid[avax][avay]+=1
            avax=elem[0]
            avay=elem[1]
            lastBox.pop()
            return
        endLose()
        return
    elif cont==0 and lastBox.size==0:
        endLose()
        return
    aux = random.choice(options)
    lastBox.push((avax,avay))
    avax+= aux[0]
    avay+= aux[1]
    if(avax==trex and avay==trey):
            endWin()
            return
    
def endWin():
    global played,doBresen,play
    print "GANASTEEEEEE"
    played=True
    doBresen=True
    play = False

def endLose():
    global played,doBresen,play
    play=False
    doBresen=True
    print "SE ACABOOOOO"
    played=True

def interface():
    background(255)
    fill(255)
    b1()
    fill(255)
    b2()
    fill(255)
    b3()
    fill(0)
    bar()
    fill(255,0,0)
    lever()
    pLever()
    fill(255)
    b4()
    update()

def update():
    global grid
    x,y=0,0;
    for row in grid:
        for col in row:
            image(grassImg,x,y,w,w)
            #if (x/w==avax and y/w==avay) or (x/w==trex and y/w==trey): grid[x/w][y/w]=0
            img = selectImg(col)
            image(img,x,y,w,w)
            x=x+w
        y=y+w
        x=0
    image(premioImg,trey*w,trex*w,w,w)
    image(avatarImg,avay*w,avax*w,w,w)

def b1():
    stroke(0)
    rect(b1x,b1y,b1w,b1h)
    textSize(20);
    fill(0)
    text("Busca!", b1x+20, b1y+20-2);

def b2():
    rect(b2x,b2y,b2w,b2h)
    image(avatarImg,b2x,b2y,b2w,b2h)
    
def b3():
    rect(b3x,b3y,b3w,b3h)
    image(premioImg,b3x,b3y,b3w,b3h)
    
def bar():
    rect(barx,bary,barw,barh)

def lever():
    global overLever
    if mouseX > levx and mouseY > levy and  mouseX < levx+levw and mouseY < levy+levh:
        overLever = True
        if not locked:
            stroke(120)
            fill(255,0,0)
    else:
        stroke(255)
        fill(255,0,0)
        overLever = False
    rect(levx,levy,levw,levh)

def pLever():
    text(str(percent) + "%", perx-8, pery);

def b4():
    global play,avax,avay,trex,trey
    fill(255)
    noStroke()
    rect(b4x,b4y,b4w,b4h)
    textSize(20);
    fill(0)
    if play==False and played:
        if avax==trex and avay==trey:
            text("ENCONTRADO", b4x+7, b4y+20-2);
        else:
            text("SUICIDIO JAJAJA", b4x+7, b4y+20-2);
            

def clearGridAvatar():
    global avax,avay
    avax=-1000/w
    avay=-1000/w

def clearGridTreasure():
    global trex,trey
    trex=-1000/w
    trey=-1000/w

def clearGrid():
    for i in range(sz):
        for j in range(sz):
            grid[i][j]=0

def putObstacles():
    global avax,avay,trex,trey
    v = [[(j,i) for i in range(0,sz)] for j in range(0,sz)]
    clearGrid()
    total=sz*sz
    objectsP=int(total*percent)/100
    if avax==trex and avay==trey:
        avax=0
        avay=0
        trex=sz-1
        trey=sz-1
    if objectsP>total-2:
        objectsP = total-2
    v[avax].remove((avax,avay))
    v[trex].remove((trex,trey))
    print objectsP
    while objectsP>0:
        aux=random.choice(v)
        while len(aux)==0:
            aux=random.choice(v)
        pos=random.choice(aux)
        if grid[pos[0]][pos[1]]!=5 and not(pos[0]==avax and pos[0]==trex) and not(pos[1]==avay and pos[1]==trey):
            grid[pos[0]][pos[1]]=5
            objectsP-=1
            aux.remove(pos)
        elif grid[pos[0]][pos[1]]!=5 and avax==trex and pos[0]==avax and pos[1]!=avay and pos[1]!=trey:
            grid[pos[0]][pos[1]]=5
            objectsP-=1
            aux.remove(pos)
        elif grid[pos[0]][pos[1]]!=5 and avay==trey and pos[1]==avay and pos[0]!=avax and pos[0]!=trex:
            grid[pos[0]][pos[1]]=5
            objectsP-=1
            aux.remove(pos)

def bresenham(x0, y0, x1, y1):
    global bresenList,iterBresen
    iterBresen=1
    aux = []
    bresenList = aux
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        #yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        bresenList.append((x0 + x*xx + y*yx, y0 + x*xy + y*yy))
        print '(' + str(x0 + x*xx + y*yx) + ',' + str(y0 + x*xy + y*yy) + ')'
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy
def mousePressed():
    global puttingTreasure, puttingAvatar,overLever,locked, yOffset,play,grid,played
    global avax,avay,trex,trey
    #print mouseY/w, mouseX/w
    if mouseX > b1x and mouseY > b1y and  mouseX < b1x+b1w and mouseY < b1y+b1h:
        played=False
        play=True
        fill(0)
        b1()
    if mouseX > b2x and mouseY > b2y and  mouseX < b2x+b2w and mouseY < b2y+b2h:
        played=False
        fill(0)
        b2()
        clearGridAvatar()
        puttingAvatar=True
    if mouseX > b3x and mouseY > b3y and  mouseX < b3x+b3w and mouseY < b3y+b3h:
        played=False
        fill(0)
        b3()
        clearGridTreasure()
        puttingTreasure=True
    if mouseX > b4x and mouseY > b4y and  mouseX < b4x+b4w and mouseY < b4y+b4h:
        played=False
        fill(0)
        b4()
        putObstacles()
    
    if overLever:
        locked = True
        fill(255,0,0)
    else:
        locked = False
        
    if (mouseX/w)<sz and (mouseY/w)<sz :
        played=False
        #noFill()
        #grid[mouseY/w][mouseX/w] = grid[mouseY/w][mouseX/w] + 1
        if grid[mouseY/w][mouseX/w] == 5:
            grid[mouseY/w][mouseX/w] =0
        else:
            grid[mouseY/w][mouseX/w] =5
        
        if puttingAvatar:
            #grid[mouseY/w][mouseX/w] = -1
            avax=mouseY/w
            avay=mouseX/w
            if(grid[avax][avay]>=0 and grid[avax][avay]<=5):
                grid[avax][avay]=0
            print "AVATAR: "+str(avax) + ' ' + str(avay)
            puttingAvatar=False
        elif puttingPremio:
            #grid[mouseY/w][mouseX/w] = -2
            trex=mouseY/w
            trey=mouseX/w
            if(grid[trex][trey]>=0 and grid[trex][trey]<=5):
                grid[trex][trey]=0
            print "TREASURE: "+str(trex) + ' ' + str(trey)
            puttingTreasure=False
    yOffset = mouseY - levy

def mouseDragged():
    global levy,percent,played
    if locked:
        played=False
        levy = mouseY - yOffset
        if levy < bary:
            levy = bary
        if levy > bary + barh:
            levy = bary + barh
        percent = (float( bary+barh-levy )*100.0) /float(barh)
        print percent
        putObstacles()

def mouseReleased():
    locked = False    
def selectImg(x):
    return {
        0: grassImg,
        1: obs1,
        2: obs2,
        3: obs3,
        4: obs4,
        5: obs5
    }.get(x, obs5)

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
     
    
                
