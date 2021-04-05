import random
import time

WIDTH=1200
HEIGHT=650
nowC=0

Game=False
Score=0
BScore=0

speed=10
Pspeed=10
col=5

key1=False
key2=False

sky=Actor("sky", (600,325))
player=Actor("player", (600,505))
coin=Actor("n1", (random.randint(50,WIDTH),-random.randint(1000,5000)))
tree=Actor("tree", (120,450))
tree2=Actor("tree", (950,450))


b=["","","","","","","","","",'']
speeds=[0,0,0,0,0,0,0,0,0,0]
e=["","","","","","","","","",'',"","","","","","","","","",'']

for i in range(0,col):
    e[i]=Actor("li", (random.randint(50,WIDTH),-random.randint(225,875)))
for i in range(0,10):
    b[i]=Actor("grass", (60+i*128,615))
    

def on_mouse_down(pos,button):
    global Game
    global Score
    global key2
    global key1
    global player
    if Game==False:
        for i in range(0,col):
            e[i]=Actor("li", (random.randint(50,WIDTH),-random.randint(225,875)))
        Score=0
        Game=True
        player.x=600
        coin.y=-random.randint(1000,5000)
        coin.x=random.randint(50,WIDTH)
    else:
        
        if pos[0]>600:
            key1=True
            a=player.x
            b=player.y
            player=Actor("player2", (a,b))
        else:
            key2=True
            a=player.x
            b=player.y
            player=Actor("player", (a,b))
def on_mouse_up(pos,button):
    global key2
    global key1
    if Game==True:
            key1=False
            key2=False

        
def on_key_down(key):

    global key1
    global key2
    global player
    if Game==True:
        if key==keys.D or key==keys.RIGHT:
            key1=True
            a=player.x
            b=player.y
            player=Actor("player2", (a,b))

        if key==keys.A or key==keys.LEFT:
            key2=True
            a=player.x
            b=player.y
            player=Actor("player", (a,b))

def on_key_up(key):
    global key1
    global key2
    global Game
    global Score
    if Game==True:
        if key==keys.D or key==keys.RIGHT:
            key1=False
        
        if key==keys.A or key==keys.LEFT:
            key2=False
    if Game==False and key==keys.SPACE:
        for i in range(0,col):
            e[i]=Actor("li", (random.randint(50,WIDTH),-random.randint(225,875)))
        Score=0
        Game=True
        player.x=600
        coin.y=-random.randint(1000,5000)
        coin.x=random.randint(50,WIDTH)
        
def anim():
    global nowC
    coin.image= "n"+str(nowC%8+1)
    nowC+=1
    clock.schedule_unique(anim,0.1)
    

def update(dt):
    global Score
    global speed
    global speeds
    global key2
    global key1
    global BScore
    global Game

    if Game==True:
        speed=10+Score/20
        coin.y+=speed-2
        if player.colliderect(coin):
            Score+=20
            coin.y=-random.randint(1000,5000)
            coin.x=random.randint(50,WIDTH)
        if key1==True:
            player.x+=Pspeed
        if key2==True:
            player.x-=Pspeed

        if player.x>WIDTH:
            player.x=0
        if player.x<0:
            player.x=WIDTH
        if coin.y>HEIGHT:
            coin.y=-random.randint(1000,5000)
            coin.x=random.randint(50,WIDTH)
        for i in range(0,col):
            e[i].y+=speed+speeds[i]
            if e[i].y>HEIGHT-125:
                Score+=1
                speeds[i]=random.randint(0,30)/10
                e[i].y=-random.randint(25,1375)
                e[i].x=random.randint(50,WIDTH)
            if player.colliderect(e[i]):

                Game=False
                key2=False
                key1=False
                if Score>BScore:
                    BScore=Score

def draw():
    sky.draw()
    tree.draw()
    tree2.draw()
    player.draw()
    if Game==False:
        screen.draw.text("Score:"+str(Score),(530,140), fontsize=60, color=(255,255,255))
        screen.draw.text("Best Score:"+str(BScore),(480,190), fontsize=60, color=(255,255,255))
        screen.draw.text("Astio",(470,20), fontsize=150, color=(255,255,255))
    else:
        coin.draw()
        for i in range(0,col):
            e[i].draw()
        screen.draw.text(str(Score),(20,15), fontsize=75, color=(255,255,255))
    for i in range(0,10):
        b[i].draw()
    if Game==False:
        screen.draw.text("Tap to start",(500,600), fontsize=60, color=(255,255,255))

anim()