import math


class Ball:
    def __init__(self, x, y, diameter, speed_x, speed_y):
        self.x = x
        self.y = y
        self.diameter = diameter
        self.speed_x = speed_x
        self.speed_y = speed_y

    """ Скорость мяча во время игры и столкновение со стенками """

    def move_ball(self):
        # left boundary
        if self.x - abs(self.speed_x) < 0:
            self.speed_x = - self.speed_x

        # right boundary
        if self.x + abs(self.speed_x) > 510:
            self.speed_x = - self.speed_x

        # up boundary
        if self.y - abs(self.speed_y) < 0:
            self.speed_y = - self.speed_y

        self.x += self.speed_x
        self.y += self.speed_y

    """ Движение мяча до нажатия клавиши мыши """

    def move_ball_to_mouse(self, mouse_x):
        self.x = mouse_x - self.diameter / 2

    """ Скорость мяча после нажатия на клавишу мыши """

    def post_click_move_ball(self):
        self.speed_y = -8

    """ Столкновение с ракеткой """

    def hit_paddle(self, paddle):
        self.speed_y = -self.speed_y
        centre_ball_x = self.x + self.diameter / 2
        centre_paddle_x = paddle.x + paddle.width_paddle / 2

        angle = (centre_ball_x - centre_paddle_x) * math.pi / 200
        new_speed_x = self.speed_x * math.cos(angle) - self.speed_y * math.sin(angle)
        new_speed_y = self.speed_x * math.sin(angle) + self.speed_y * math.cos(angle)

        self.speed_x = new_speed_x
        self.speed_y = new_speed_y
        self.y -= 5

    """ Столкновение с кирпичом """

    def hit_brick(self, brick):
        if self.y + self.diameter <= brick.y + brick.height_brick / 2 \
                or self.y > brick.y + brick.height_brick / 2:
            self.speed_y = -self.speed_y
        else:
            self.speed_x = -self.speed_x
