import random

WIDTH = HEIGHT = 500

lastTime = 0
currentTime = 0
hero = Actor('razorinv')
hero.x, hero.y = WIDTH // 2, HEIGHT // 2

enemies = []
enemycd = 2

# Пули
bullets = []
isShot = False
t = 0
lost = False

def on_key_down(key):
    global isShot
    if key == keys.space:
        isShot = True


def update(dt):
    global lost, enemies, isShot, t, bullets

    for enemy in enemies:
        if hero.colliderect(enemy):
            lost = True

    nenemies = [e for e in enemies if e.collidelist(bullets) == -1]
    nbullets = [b for b in bullets if b.collidelist(enemies) == -1 and b.bottom > -5]
    enemies, bullets = nenemies, nbullets

    if isShot:
        bullets.append(Actor('bullet', pos=(hero.left + 33, hero.top + 5)))
        isShot = False

    if t > enemycd:
        x = random.randint(0, WIDTH)
        enemies.append(Actor('invaderinv', pos=(x, 20)))
        t = 0

    if keyboard.left and hero.left > 0:
        hero.left -= 5
    if keyboard.right and hero.right < WIDTH:
        hero.left += 5
    if keyboard.up and hero.top > 0:
        hero.top -= 5
    if keyboard.down and hero.bottom < HEIGHT:
        hero.top += 5

    t += dt

def draw():
    global lost

    screen.fill('black')
    if not lost:
        hero.draw()
        for bullet in bullets:
            bullet.draw()
            bullet.top -= 5
        for enemy in enemies:
            enemy.draw()
            enemy.top += 2
    else:
        screen.draw.text('GAME OVER', 
                         pos=(200, 200), 
                         sysfontname='comic sans ms', 
                         color='red',
                         fontsize=50) 