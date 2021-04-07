from random import randint as rand

WIDTH = 500
HEIGHT = 500

N = 100
R = 10
GLAZA = 0
LUG = (GLAZA + 1) / 2
CHASTOTA = 1
SPEED = 20
CL = (255, 255, 255)
zzz = [Actor('s_1', (0, 0)) for q in range(N)]
xxx = [-1 * (R // 2) for q in range(WIDTH)]
print(len(xxx))
veter = 0
for q in range(N):
    zzz[q].ris = False


def on_key_down():
    global veter

    if keyboard.LEFT:
        veter -= 1
    elif keyboard.RIGHT:
        veter += 1


def stolb(n, dlin, test):
    screen.draw.filled_circle((n + (R // 2), HEIGHT - dlin), R // 2, CL)
    screen.draw.filled_rect(Rect((n, HEIGHT), (R, -1 * dlin)), CL)


def sglaz():
    global xxx

    for q in range(CHASTOTA):
        for q in range(1, len(xxx)):
            if xxx[q] - xxx[q - 1] > GLAZA:
                xxx[q - 1] += LUG
                xxx[q] -= LUG
            if xxx[q - 1] - xxx[q] > GLAZA:
                xxx[q - 1] -= LUG
                xxx[q] += LUG


def update(dt):
    global zzz, veter, xxx

    if not (keyboard.SPACE):

        for q in range(N):
            if zzz[q].ris:
                zzz[q].x += rand(-1, 1) + veter
                zzz[q].y += rand(-1, 1) + SPEED

                if zzz[q].x > 0 and zzz[q].x < WIDTH:
                    if zzz[q].y > (HEIGHT - xxx[int(zzz[q].x)] - 5):
                        zzz[q].ris = False
                        xxx[(int(zzz[q].x) - 3) % len(xxx)] += 6
                        xxx[int(zzz[q].x)] += 8
                        xxx[(int(zzz[q].x) + 3) % len(xxx)] += 6

                elif zzz[q].y > HEIGHT:
                    zzz[q].ris = False
            else:
                zzz[q].x = rand(-5 - (veter * HEIGHT // SPEED),
                                WIDTH + 5 - (veter * HEIGHT // SPEED))
                zzz[q].y = rand(0 - HEIGHT, -10)
                zzz[q].ris = True

    sglaz()


def draw():
    global zzz, xxx
    screen.clear()
    for q in range(N):
        if zzz[q].ris:
            zzz[q].draw()

    for q in range(len(xxx)):
        stolb(q, xxx[q], q)
