import unittest

from model.ball import Ball
from model.brick import Brick
from model.game import Game
from model.paddle import Paddle


class TestPaddleMethods(unittest.TestCase):
    def setUp(self):
        self.paddle = Paddle(x=0, y=0, width_paddle=100, height_paddle=20)

    def test_calc_coords_paddle(self):
        self.assertEqual(self.paddle.x, 0)
        self.assertEqual(self.paddle.y, 0)
        self.assertEqual(self.paddle.width_paddle, 100)
        self.assertEqual(self.paddle.height_paddle, 20)

    def test_move_paddle(self):
        self.paddle.move_paddle(100)
        self.assertEqual(self.paddle.x, 50)

        self.paddle.move_paddle(0)
        self.assertEqual(self.paddle.x, -50)


class TestBallMethods(unittest.TestCase):
    def setUp(self):
        self.ball = Ball(300, 300, 14, -5, 5)

    def test_move_ball(self):
        self.ball.move_ball()
        self.assertEqual(self.ball.x, 295)
        self.assertEqual(self.ball.y, 305)

    def test_move_ball_to_mouse(self):
        self.ball.move_ball_to_mouse(49)
        self.assertEqual(self.ball.x, 42)
        self.assertEqual(self.ball.y, 300)

    def test_post_click_move_ball(self):
        self.ball = Ball(300, 300, 14, 0, 0)
        self.ball.post_click_move_ball()
        self.assertEqual(self.ball.speed_y, -10)
        self.assertEqual(self.ball.speed_x, 0)

    def test_hit_boundaries(self):
        ""
        """ Удар в левую стенку """
        self.ball.x = 0
        self.ball.speed_x = -5
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_x, 5)
        self.assertEqual(self.ball.x, 5)

        self.ball.x = -3
        self.ball.speed_x = -5
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_x, 5)
        self.assertEqual(self.ball.x, 2)

        """ Удар в правую стенку """
        self.ball.x = 510
        self.ball.speed_x = 5
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_x, -5)
        self.assertEqual(self.ball.x, 505)

        self.ball.x = 514
        self.ball.speed_x = 5
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_x, -5)
        self.assertEqual(self.ball.x, 509)

        """ Удар в верхнюю стенку """
        self.ball.y = 0
        self.ball.speed_y = -6
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_y, 6)
        self.assertEqual(self.ball.y, 6)

        self.ball.y = -5
        self.ball.speed_y = -8
        self.ball.move_ball()
        self.assertEqual(self.ball.speed_y, 8)
        self.assertEqual(self.ball.y, 3)

    def test_hit_paddle_left(self):
        self.paddle = Paddle(100, 300, 100, 20)

        """ Удар в левый край ракетки слева """
        self.ball = Ball(100, 286, 14, 5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 0.7759)
        self.assertEqual(round(self.ball.speed_y, 4), -7.0284)
        self.assertEqual(self.ball.y, 281)

        """ Удар в правый край ракетки слева """
        self.ball = Ball(200, 286, 14, 5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 7.0284)
        self.assertEqual(round(self.ball.speed_y, 4), 0.7759)
        self.assertEqual(self.ball.y, 281)

        """ Удар в середину ракетки слева """
        self.ball = Ball(143, 286, 14, 5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 5)
        self.assertEqual(round(self.ball.speed_y, 4), -5)
        self.assertEqual(self.ball.y, 281)

        """ Удар между левым краем и серединой ракетки слева """
        self.ball = Ball(125, 286, 14, 5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 3.4065)
        self.assertEqual(round(self.ball.speed_y, 4), -6.1964)
        self.assertEqual(self.ball.y, 281)

        """ Удар между правым краем и серединой ракетки слева """
        self.ball = Ball(175, 286, 14, 5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 6.7903)
        self.assertEqual(round(self.ball.speed_y, 4), -1.9728)
        self.assertEqual(self.ball.y, 281)

    def test_hit_paddle_right(self):
        self.paddle = Paddle(100, 300, 100, 20)

        """ Удар в левый край ракетки справа """
        self.ball = Ball(100, 286, 14, -5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), -7.0284)
        self.assertEqual(round(self.ball.speed_y, 4), -0.7759)
        self.assertEqual(self.ball.y, 281)

        """ Удар в правый край ракетки справа """
        self.ball = Ball(200, 286, 14, -5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), 0.7759)
        self.assertEqual(round(self.ball.speed_y, 4), -7.0284)
        self.assertEqual(self.ball.y, 281)

        """ Удар в середину ракетки справа """
        self.ball = Ball(143, 286, 14, -5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), -5)
        self.assertEqual(round(self.ball.speed_y, 4), -5)
        self.assertEqual(self.ball.y, 281)

        """ Удар между левым краем и серединой ракетки справа """
        self.ball = Ball(125, 286, 14, -5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), -6.1964)
        self.assertEqual(round(self.ball.speed_y, 4), -3.4065)
        self.assertEqual(self.ball.y, 281)

        """ Удар между правым краем и серединой ракетки справа """
        self.ball = Ball(175, 286, 14, -5, 5)
        self.ball.hit_paddle(self.paddle)
        self.assertEqual(round(self.ball.speed_x, 4), -1.9728)
        self.assertEqual(round(self.ball.speed_y, 4), -6.7903)
        self.assertEqual(self.ball.y, 281)

    def test_hit_brick(self):
        ""
        """ Удар мяча по кирпичу снизу """
        self.ball = Ball(200, 200, 14, 4, -6)
        self.brick = Brick(180, 180, 1)
        self.ball.hit_brick(self.brick)
        self.assertEqual(self.ball.speed_x, 4)
        self.assertEqual(self.ball.speed_y, 6)

        """ Удар мяча по кирпичу сверху """
        self.ball = Ball(200, 200, 14, 6, 4)
        self.brick = Brick(180, 220, 1)
        self.ball.hit_brick(self.brick)
        self.assertEqual(self.ball.speed_x, 6)
        self.assertEqual(self.ball.speed_y, -4)

        """ Удар мяча по кирпичу слева """
        self.ball = Ball(200, 200, 14, 5, 5)
        self.brick = Brick(214, 200, 1)
        self.ball.hit_brick(self.brick)
        self.assertEqual(self.ball.speed_x, -5)
        self.assertEqual(self.ball.speed_y, 5)

        """ Удар мяча по кирпичу справа """
        self.ball = Ball(200, 200, 14, -5, 5)
        self.brick = Brick(160, 200, 1)
        self.ball.hit_brick(self.brick)
        self.assertEqual(self.ball.speed_x, 5)
        self.assertEqual(self.ball.speed_y, 5)


class TestBrickMethods(unittest.TestCase):
    def setUp(self):
        self.bricks = []

    def test_break_brick(self):
        brick = Brick(250, 400, 1)
        self.bricks.append(Brick(250, 400, 1))
        length = len(self.bricks)
        self.assertEqual(length, 1)
        self.assertEqual(1, self.bricks[0].brick_health)
        for el in self.bricks:
            if brick.x == el.x and brick.y == el.y:
                el.break_brick(el, self.bricks)
                self.assertEqual(0, el.brick_health)
                break
        self.assertLess(len(self.bricks), length)

    def test_check_on_brick_health(self):
        self.bricks = [Brick(250, 400, 1), Brick(250, 340, 2), Brick(250, 300, 3)]

        el = self.bricks[0]
        self.assertEqual(1, el.brick_health)
        el.break_brick(el, self.bricks)
        self.assertEqual(0, el.brick_health)

        el = self.bricks[0]
        self.assertEqual(2, el.brick_health)
        el.break_brick(el, self.bricks)
        self.assertEqual(1, el.brick_health)

        el = self.bricks[1]
        self.assertEqual(3, el.brick_health)
        el.break_brick(el, self.bricks)
        self.assertEqual(2, el.brick_health)

    def test_multiple_hit(self):
        self.bricks = [Brick(250, 300, 3)]
        el = self.bricks[0]

        self.assertEqual(3, el.brick_health)

        el.break_brick(el, self.bricks)
        el.break_brick(el, self.bricks)
        el.break_brick(el, self.bricks)

        self.assertEqual(0, el.brick_health)
        self.assertEqual(0, len(self.bricks))

    def test_brick_invisibility(self):
        self.bricks = [Brick(250, 260, 3, True)]
        self.assertTrue(self.bricks[0].is_invisibility)

        self.bricks = [Brick(100, 100, 3)]
        self.assertFalse(self.bricks[0].is_invisibility)


class TestGameMethods(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.start_game()

    def test_start_game(self):
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.paddle.x, 210)
        self.assertEqual(self.game.ball.y, 436)
        self.assertEqual(self.game.ball.speed_x, 0)

    def test_lose_life(self):
        self.game.lives = 2
        self.game.ball.y = 680
        self.game.check_on_lose_life()
        self.assertEqual(self.game.lives, 1)
        self.assertFalse(self.game.is_init_game)

    def test_level_completed(self):
        self.game.bricks = [Brick(0, 0, 1)]
        self.assertFalse(self.game.level_completed())

        self.game.bricks.clear()
        self.assertTrue(self.game.level_completed())

    def test_game_completed(self):
        self.game.bricks = [Brick(0, 0, 1)]
        self.game.level_number = self.game.level.max_level_number
        self.assertFalse(self.game.game_completed())

        self.game.bricks = []
        self.game.level_number = self.game.level.max_level_number
        self.assertTrue(self.game.game_completed())

        self.game.bricks = []
        self.game.level_number = 1
        self.game.level.max_level_number = 3
        self.assertFalse(self.game.game_completed())

    def test_game_over(self):
        self.game.lives = 0
        self.assertTrue(self.game.game_over())

        self.game.lives = 1
        self.assertFalse(self.game.game_over())

        self.game.lives = 1
        self.game.ball.y = 680
        self.game.check_on_lose_life()
        self.assertTrue(self.game.game_over())

    def test_post_click_game(self):
        self.game.is_init_game = False
        self.game.post_click_game()
        self.assertTrue(self.game.is_init_game)

        self.game.is_init_game = True
        self.game.post_click_game()
        self.assertTrue(self.game.is_init_game)
