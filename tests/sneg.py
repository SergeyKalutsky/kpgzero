from random import randint as rand

WIDTH = 800
HEIGHT = 600

N = 100
R = 10

CL = (255, 255, 255)

zzz = [Actor('s_1', (0, 0)) for q in range(N)]
xxx = [0 for q in range(WIDTH // R)]

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


def stolb(n, dlin, a):
    screen.draw.filled_rect(
        Rect((n * R, HEIGHT), ((n + 1) * R, HEIGHT - dlin)), CL)
    screen.draw.filled_circle((n * R + (R // 2), HEIGHT - dlin), R // 2, CL)


def update():
    global zzz, veter
    for q in range(N):
        if zzz[q].ris:
            zzz[q].x += rand(-1, 1) + veter
            zzz[q].y += rand(-1, 1) + 5

            if zzz[q].y > (HEIGHT - xxx[int(zzz[q].x // (WIDTH // R))]):
                zzz[q].ris = False

                xxx[int(zzz[q].x // (WIDTH // R))] += 1
        else:
            zzz[q].x = rand(-5 - (veter * HEIGHT // 5),
                            WIDTH + 5 - (veter * HEIGHT // 5))
            zzz[q].y = rand(0 - HEIGHT, -10)
            zzz[q].ris = True


def draw():
    global zzz, xxx
    screen.clear()
    for q in range(N):
        if zzz[q].ris:
            zzz[q].draw()

    for q in range(len(xxx)):
        stolb(q, xxx[q], q)
