from model.ball import Ball
from model.levels import Level
from model.paddle import Paddle


class Game:
    def __init__(self):
        self.bricks = []
        self.is_init_game = False
        self.level_number = 1
        self.score = 0
        self.lives = 3
        self.level = Level()

    """ Состояние начала игры """

    def start_game(self):
        self.bricks.clear()
        self.paddle = Paddle(210, 450, 100, 20)
        self.ball = Ball(253, 436, 14, 0, 0)
        self.is_init_game = False
        self.bricks = self.level.parser(self.level_number)

    """ Начало игры после нажатия клавиши мыши """

    def post_click_game(self):
        if not self.is_init_game:
            self.is_init_game = True
            self.ball.post_click_move_ball()

    """ Потеря жизни """

    def check_on_lose_life(self):
        if self.ball.y >= 480:
            self.is_init_game = False
            self.lives -= 1
            self.ball = Ball(
                x=self.paddle.x + self.paddle.width_paddle / 2 - self.ball.diameter / 2,
                y=self.paddle.y - self.ball.diameter,
                diameter=14,
                speed_x=0,
                speed_y=0
            )

    """ Игра пройдена """

    def game_completed(self):
        return self.level_completed() and self.level_number == self.level.max_level_number

    """ Проигрыш """

    def game_over(self):
        return self.lives == 0

    """ Уровень пройден """

    def level_completed(self):
        return len(self.bricks) == 0
