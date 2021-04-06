from random import randint


def get_pos(size): 
    return randint(0, size - FSIZE)

WIDTH = 400
HEIGHT = 400
NEWFOOD = 40
FSIZE = 20


foodCounter = 0

player = Rect(300, 100, 50, 50)
foods = [Rect(get_pos(WIDTH), get_pos(HEIGHT), FSIZE, FSIZE) for _ in range(20)]

SPEED = 10

def update(dt):
    global foods, foodCounter, moving, player

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(Rect(get_pos(WIDTH), get_pos(HEIGHT), FSIZE, FSIZE))

    if keyboard.left and player.left > 0:
        player.left -= SPEED
    if keyboard.right and player.right < WIDTH:
        player.right += SPEED
    if keyboard.up and player.top > 0:
        player.top -= SPEED
    if keyboard.down and player.bottom < HEIGHT:
        player.top += SPEED

    for food_col in foods:
        if player.colliderect(food_col):
            foods.remove(food_col) 

def draw():
    screen.fill('white')
    screen.draw.filled_rect(player, 'green')
    for food in foods:
        screen.draw.filled_rect(food, 'red') 