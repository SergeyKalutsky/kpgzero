from random import randint as rnd
from random import choice as ch
from time import time

WIDTH = 600
HEIGHT = 600
ship = Actor('starship', (300, 500))
buls = []
aliens = []
flag_0 = True
flag_1 = 0
flag_3 = False
t1 = time()
t2 = 0
for i in range(20, 221, 40):
    for j in range(75, 526, 50):
        alien = Actor('alien_enemy', (j, i))
        aliens.append(alien)
b = ch(aliens)
bomb = Actor('bomb_gx2', (b.x, b.y))

def shot(x):
    global flag_1
    if flag_1 == 0:
        bullet = Actor('laser', (x, 480))
        buls.append(bullet)
        flag_1 = 1
        clock.schedule(rec_1, 0.5)

def move():
    xx = [i.x for i in aliens]
    if not 575 in xx and not 25 in xx:
        c = rnd(1, 3)
    elif not 575 in xx:
        c = rnd(1, 2)
        if c == 2:
            c = 3
    elif not 25 in xx:
        c = rnd(1, 2)
    else:
        c = 1
    for i in aliens:
        if c == 1:
            i.y += 40
        elif c == 2:
            i.x -= 50
        elif c == 3:
            i.x += 50

def bum():
    global bomb
    b = ch(aliens)
    bomb = Actor('bomb', (b.x, b.y))

clock.schedule_interval(bum, 4)
clock.schedule_interval(move, 2)

def rec_1():
    global flag_1
    flag_1 = 0

def draw():
    screen.clear()
    screen.draw.text('Your score: ', (0, 520), color=(0, 0, 255), fontsize=40)
    screen.draw.text('Your time: ', (0, 560), color=(0, 0, 255), fontsize=40)
    screen.draw.text(str(t2), (150, 560), color=(0, 0, 255), fontsize=40)
    if flag_0:
        ship.draw()
        bomb.draw()
        for i in buls:
            i.draw()
        for i in aliens:
            i.draw()
    else:
        if flag_3:
            screen.draw.text('You win!', (150, 250), color=(255, 255, 0), fontsize=100)
        else:
            screen.draw.text('Game Over', (100, 250), color=(0, 255, 0), fontsize=100)

def update():
    global flag_0, ship, buls, aliens, bomb, flag_1, flag_3, t1, t2
    if flag_0:
        t2 = int((time()-t1)//1)
    if keyboard.LEFT and ship.x > 29:
        ship.x -= 5
    if keyboard.RIGHT and ship.x < 571:
        ship.x += 5
    if keyboard.SPACE:
        shot(ship.x)
    for i in buls:
        i.y -= 5
        if i.y < 0:
            buls.remove(i)
    bomb.y += 10
    for i in buls:
        for j in aliens:
            if i.colliderect(j):
                if i in buls and j in aliens:
                    buls.remove(i)
                    aliens.remove(j)
    if len(aliens) == 0:
        flag_0 = False
        flag_3 = True
    for i in aliens:
        if i.colliderect(ship):
            flag_0 = False
    if bomb.colliderect(ship):
        flag_0 = False
    if (not flag_0) and keyboard.Z:
        ship = Actor('starship', (300, 500))
        buls = []
        aliens = []
        flag_0 = True
        flag_1 = 0
        flag_3 = False
        t1 = time()
        t2 = 0
        for i in range(20, 221, 40):
            for j in range(75, 526, 50):
                alien = Actor('alien_enemy', (j, i))
                aliens.append(alien)
        b = ch(aliens)
        bomb = Actor('bomb_gx2', (b.x, b.y))