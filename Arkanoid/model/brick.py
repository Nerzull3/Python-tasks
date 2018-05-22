class Brick:
    def __init__(self, x, y, brick_health, invisibility=False):
        self.x = x
        self.y = y
        self.brick_health = brick_health
        self.is_invisibility = invisibility
        self.width_brick = 40
        self.height_brick = 20

    """ Разрушение кирпича """

    def break_brick(self, brick, bricks):
        self.brick_health -= 1
        if self.brick_health == 0:
            bricks.remove(brick)
