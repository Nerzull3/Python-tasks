class Paddle:
    def __init__(self, x, y, width_paddle, height_paddle):
        self.x = x
        self.y = y
        self.width_paddle = width_paddle
        self.height_paddle = height_paddle

    """ Движение ракетки во время игры """
    def move_paddle(self, mouse_x):
        self.x = mouse_x - self.width_paddle / 2
