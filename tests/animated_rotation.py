import random

WIDTH = 400
HEIGHT = 400


BLOCK_POSITIONS = [
    (350, 50),
    (350, 350),
    (50, 350),
    (50, 50),
]
block_id = 0

block = Actor('block', center=(50, 50))
ship = Actor('ship', center=(200, 200))


def draw():
    screen.clear()
    block.draw()
    ship.draw()


# Block movement
# --------------

def move_block():
    """Move the block to the next position over 1 second."""
    block_id %= 4
    animate(
        block,
        'bounce_end',
        duration=1,
        pos=BLOCK_POSITIONS[block_id]
    )


def next_ship_target():
    """Pick a new target for the ship and rotate to face it."""
    x = random.randint(100, 300)
    y = random.randint(100, 300)
    ship.target = x, y

    target_angle = ship.angle_to(ship.target)
    target_angle += 360 * ((ship.angle - target_angle + 180) // 360)

    animate(
        ship,
        angle=target_angle,
        duration=0.3,
        on_finished=move_ship,
    )


def move_ship():
    """Move the ship to the target."""
    anim = animate(
        ship,
        tween='accel_decel',
        pos=ship.target,
        duration=ship.distance_to(ship.target) / 200,
        on_finished=next_ship_target,
    )


next_ship_target()
move_block()  # start one move now
clock.schedule_interval(move_block, 2)  # schedule subsequent moves
