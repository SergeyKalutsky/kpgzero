from random import randint as rnd
from time import time as t

HEIGHT = 600
WIDTH = 600
b = 10
col = [(192, 192, 192), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 128), (0, 128, 0), (128, 0, 0), (128, 128, 0), (128, 0, 128)]
au = [[0 for i in range(10)] for j in range(10)]
ac = [[0 for i in range(10)] for j in range(10)]
gg = 0
s = 0
ti = ''
t1 = int(t()//1)
while s < b:
    yr = rnd(0, 10-1)
    xr = rnd(0, 10-1)
    if au[yr][xr] != -1:
        au[yr][xr] = -1
        s += 1
        if xr < 9 and au[yr][xr+1] != -1:
            au[yr][xr+1] += 1
        if xr > 0 and au[yr][xr-1] != -1:
            au[yr][xr-1] += 1
        if yr < 9 and au[yr+1][xr] != -1:
            au[yr+1][xr] += 1
        if yr > 0 and au[yr-1][xr] != -1:
            au[yr-1][xr] += 1
        if xr < 9 and yr < 9 and au[yr+1][xr+1] != -1:
            au[yr+1][xr+1] += 1
        if xr < 9 and yr > 0 and au[yr-1][xr+1] != -1:
            au[yr-1][xr+1] += 1
        if xr > 0 and yr < 9 and au[yr+1][xr-1] != -1:
            au[yr+1][xr-1] += 1
        if xr > 0 and yr > 0 and au[yr-1][xr-1] != -1:
            au[yr-1][xr-1] += 1

def draw():
    global col,t1,ti
    screen.clear()
    screen.fill((255, 255, 255))
    for i in range(50, 551, 50):
        screen.draw.line((i, 50), (i, 550), (0, 0, 0))
    for i in range(50, 551, 50):
        screen.draw.line((50, i), (550, i), (0, 0, 0))
    for i in range(10):
        for j in range(10):
            if ac[i][j] == 1 and au[i][j] != -1:
                screen.draw.text(str(au[i][j]), ((j+2)*50-30, (i+2)*50-30), color=col[au[i][j]], fontsize=40)
            elif ac[i][j] == 1 and au[i][j] == -1:
                screen.blit('bomb', ((j+1)*50+5, (i+1)*50+5))
            elif ac[i][j] == 2:
                screen.blit('flag', ((j+1)*50+5, (i+1)*50+5))
    screen.draw.line((150, 0), (150, 50), (0, 0, 0))
    screen.draw.line((450, 0), (450, 50), (0, 0, 0))
    screen.draw.line((250, 0), (250, 50), (0, 0, 0))
    screen.draw.line((350, 0), (350, 50), (0, 0, 0))
    screen.draw.line((150, 0), (450, 0), (0, 0, 0))
    screen.draw.text('Новая игра', (355, 20), color=(0, 0, 255), fontsize=24)
    if gg == 1:
        screen.draw.text('Победа!', (165, 20), color=(0, 255, 0), fontsize=24)
    elif gg == 2:
        screen.draw.text('Поражение!', (152, 20), color=(255, 0, 0), fontsize=24)
    else:
        screen.draw.text('Игра идёт...', (160, 20), color=(128, 128, 128), fontsize=20)
        t2 = int(t()//1)
        ti = str((t2-t1)//60)+':'+str((t2-t1)%60)
        if ((t2-t1)%60)<10:
            ti = ti[:-1]+'0'+ti[-1]
        if (t2-t1)//60<10:
            ti = '0'+ti
    screen.draw.text(ti, (280, 20), color=(0, 0, 0), fontsize=25)

def on_mouse_down(button, pos):
    global gg,au,ac,s,b,t1
    x = pos[0]
    y = pos[1]
    x = x//50-1
    y = y//50-1
    if -1<x<10 and -1<y<10:
        if button == mouse.LEFT and ac[y][x] == 0:
            k = kl(y, x)
            if k == -1 and gg == 0:
                for i in range(10):
                    for j in range(10):
                        ac[i][j] = 1
                gg = 2
        elif button == mouse.RIGHT and ac[y][x] == 0:
            ac[y][x] = 2
        elif button == mouse.RIGHT and ac[y][x] == 2:
            ac[y][x] = 0
    if 350<pos[0]<450 and 0<pos[1]<50:
        au = [[0 for i in range(10)] for j in range(10)]
        ac = [[0 for i in range(10)] for j in range(10)]
        t1 = int(t()//1)
        gg = 0
        s = 0
        while s < b:
            yr = rnd(0, 10-1)
            xr = rnd(0, 10-1)
            if au[yr][xr] != -1:
                au[yr][xr] = -1
                s += 1
                if xr < 9 and au[yr][xr+1] != -1:
                    au[yr][xr+1] += 1
                if xr > 0 and au[yr][xr-1] != -1:
                    au[yr][xr-1] += 1
                if yr < 9 and au[yr+1][xr] != -1:
                    au[yr+1][xr] += 1
                if yr > 0 and au[yr-1][xr] != -1:
                    au[yr-1][xr] += 1
                if xr < 9 and yr < 9 and au[yr+1][xr+1] != -1:
                    au[yr+1][xr+1] += 1
                if xr < 9 and yr > 0 and au[yr-1][xr+1] != -1:
                    au[yr-1][xr+1] += 1
                if xr > 0 and yr < 9 and au[yr+1][xr-1] != -1:
                    au[yr+1][xr-1] += 1
                if xr > 0 and yr > 0 and au[yr-1][xr-1] != -1:
                    au[yr-1][xr-1] += 1

def kl(y1, x1):
    ac[y1][x1] = 1
    if au[y1][x1] == 0:
        if x1 < 9 and ac[y1][x1+1] == 0:
            c = kl(y1, x1+1)
        if x1 > 0 and ac[y1][x1-1] == 0:
            c = kl(y1, x1-1)
        if y1 < 9 and ac[y1+1][x1] == 0:
            c = kl(y1+1, x1)
        if y1 > 0 and ac[y1-1][x1] == 0:
            c = kl(y1-1, x1)
        if x1 < 9 and y1 < 9 and ac[y1+1][x1+1] == 0:
            c = kl(y1+1, x1+1)
        if x1 < 9 and y1 > 0 and ac[y1-1][x1+1] == 0:
            c = kl(y1-1, x1+1)
        if x1 > 0 and y1 < 9 and ac[y1+1][x1-1] == 0:
            c = kl(y1+1, x1-1)
        if x1 > 0 and y1 > 0 and ac[y1-1][x1-1] == 0:
            c = kl(y1-1, x1-1)
    elif au[y1][x1] == -1:
        return -1
    else:
        return 0
    return 0

def update(dt):
    global gg
    nb = 0
    for i in range(10):
        for j in range(10):
            if ac[i][j] == 1:
                nb += 1
    if nb == 90:
        for i in range(10):
            for j in range(10):
                ac[i][j] = 1
        gg = 1
