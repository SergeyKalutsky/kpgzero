import pygame
import random

#Настройки окна
WIDTH = 300
HEIGHT = 500

CARHEIGHT = 70
SPEED = 2


CARHEIGHT = 70
SPEED = 5

car_hero = Actor('car')
car_hero.x, car_hero.y = 150, 450

car_enemy = Actor('carenemy')
y_enemy = 0 - CARHEIGHT
x_enemy = random.choice([10, 130, 250])
car_enemy.x, car_enemy.y = x_enemy, y_enemy

def update(dt):
    global SPEED, lost
    lost = car_hero.colliderect(car_enemy)
    if not lost:
        if car_enemy.top >= HEIGHT + CARHEIGHT:
            SPEED += 0.7
            car_enemy.top = 0 - CARHEIGHT
            car_enemy.left = random.choice([10, 130, 250])
        else:
            # Прибавление скорости
            car_enemy.top += SPEED

        if keyboard.left:
            if car_hero.left > -10:
                car_hero.left -= 10
        if keyboard.right:
            if car_hero.left < 250:
                car_hero.left += 10

def draw():
    global lost
    screen.fill('white')
    car_hero.draw()
    car_enemy.draw()
    if lost:
        screen.draw.text('GAME OVER', pos=(80, 200), fontsize=35, color='RED')
