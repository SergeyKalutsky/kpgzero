import random
import time


WIDTH = 800
HEIGHT = 500
FPS = 30
elems = []
score = 0

obj = Actor('2')
obj.pos = random.randint(60, 730), random.randint(60, 430)

elem = Actor('1')
elem.x = 400
elem.y = 400
elems.append(elem)

game_over = False

def add_elem():
    global elems, score
    elem = Actor('1')
    elem.x = elems[-1].x
    elem.y = elems[-1].y+elem.width
    elems.append(elem)
    score += 1


for i in range(2):
    add_elem()
    score -= 1
vx = 0
vy = -elems[0].width


def draw():
    screen.clear()
    for i in range(len(elems)):
        elems[i].draw()
    obj.draw()
    screen.draw.text("Score: {}".format(score), (20, 20), fontsize=30)


def update(dt):
    global vx, vy, elems, game_over
    if not game_over:
        prev = elems[0].pos
        elems[0].x += vx
        elems[0].y += vy
        for i in range(1, len(elems)):
            preprev = elems[i].pos
            elems[i].pos = prev
            prev = preprev
        if keyboard.left:
            vx = -elems[0].width
            vy = 0
        if keyboard.right:
            vx = elems[0].width
            vy = 0
        if keyboard.up:
            vx = 0
            vy = -elems[0].width
        if keyboard.down:
            vx = 0
            vy = elems[0].width
        if elems[0].x > WIDTH:
            game_over = True
        if elems[0].x < 0:
            game_over = True
        if elems[0].y > HEIGHT:
            game_over = True
        if elems[0].y < 0:
            game_over = True
        if elems[0].colliderect(obj):
            add_elem()
            obj.pos = random.randint(10, 790), random.randint(10, 490)
        for i in range(1, len(elems)):
            if elems[0].colliderect(elems[i]):
                game_over = True
        time.sleep(0.1)