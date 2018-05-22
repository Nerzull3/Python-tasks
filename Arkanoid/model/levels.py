from model.brick import Brick


class Level:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.bricks = []
        self.read_line = -1
        self.max_level_number = 0

    def get_lines(self):
        with open(r'.\model\initialize_map') as f:
            self.bricks.clear()
            for i, line in enumerate(f):
                if i <= self.read_line:
                    continue
                elif line == '\n':
                    self.read_line = i
                    break

                self.read_line = i
                self.bricks.append(line[:-1])
            return self.bricks

    def parser(self, level_number):
        result = Level()

        self.bricks = self.get_lines()

        if len(self.bricks) == 0:
            self.max_level_number = level_number
        else:
            self.width = len(self.bricks[0])
            self.height = len(self.bricks)

            for y in range(self.height):
                for x in range(self.width):
                    if self.bricks[y][x] == '1':
                        result.bricks.append(Brick(x * 40, y * 20, 1))
                    elif self.bricks[y][x] == '2':
                        result.bricks.append(Brick(x * 40, y * 20, 2))
                    elif self.bricks[y][x] == '3':
                        result.bricks.append(Brick(x * 40, y * 20, 3))
                    elif self.bricks[y][x] == '4':
                        result.bricks.append(Brick(x * 40, y * 20, 4))
                    elif self.bricks[y][x] == '5':
                        result.bricks.append(Brick(x * 40, y * 20, 2, True))

        return result.bricks
