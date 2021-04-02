WIDTH, HEIGHT = 500, 500

mouse_down, changed, minus = False, False, False
indx, r, update_r = 1, 1, 1
colors = ['red', 'white', 'blue', 'yellow', 'green']
color = colors[0]


def on_mouse_down(button, pos):
    global mouse_down, indx, color
    if button == 1:
        mouse_down = True if not mouse_down else False
    if button == 3:
        color = colors[indx % 5]
        indx += 1
        screen.draw.text('Выбран цвет:  ' + color+'          ', 
                         pos=(150, 10), 
                         color='black', 
                         background='white')


def on_key_down(key):
    global changed, r, minus
    if key == keys.down:
        changed = True
        minus = True
        update_r = 1 if r !=0 else 0

    if key == keys.up:
        changed = True
        update_r = 1 if r != 15 else 0


def on_mouse_move(pos):
    global mouse_down, color
    if mouse_down:
        screen.draw.filled_circle(pos, r, color)


def update(dt):
    global changed, r, minus
    if changed:
        if minus:
            r -= update_r
            minus = False
        else:
            r += update_r
        screen.draw.text('Размер пера:  ' + str(r) +'          ', 
                         pos=(150, 10), 
                         color='black', 
                         background='white')
        changed = False

