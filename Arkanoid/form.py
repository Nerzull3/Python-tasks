import tkinter
import tkinter.messagebox as message_box

# import simpleaudio
from PIL import Image, ImageTk

from model.game import Game

WIDTH = 520
HEIGHT = 600


class Form(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self.title("Arkanoid")
        self.resizable(width=False, height=False)
        self.canvas = tkinter.Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.canvas.bind('<Motion>', self.__on_mouse_event)
        self.canvas.bind('<Button-1>', self.__on_mouse_click)

        self.images = [get_image(r'.\images\background.png'),
                       get_image(r'.\images\paddle_blue.png'),
                       get_image(r'.\images\brick_yellow.png'),
                       get_image(r'.\images\brick_blue.png'),
                       get_image(r'.\images\brick_purple.png'),
                       get_image(r'.\images\brick_grey.png'),
                       get_image(r'.\images\brick_red.png'),
                       get_image(r'.\images\ball.png')]

        self.image_bg = ImageTk.PhotoImage(self.images[0])  # background image
        self.canvas.create_image(0, 0, image=self.image_bg, anchor='nw')

        self.image_paddle = ImageTk.PhotoImage(self.images[1])
        self.image_bricks = [ImageTk.PhotoImage(self.images[2]),
                             ImageTk.PhotoImage(self.images[3]),
                             ImageTk.PhotoImage(self.images[4]),
                             ImageTk.PhotoImage(self.images[5]),
                             ImageTk.PhotoImage(self.images[6])]
        self.image_ball = ImageTk.PhotoImage(self.images[7])

        # self.music = [get_wave_object(r'.\audio\music\Arkanoid_SoundTrack_1.wav'),  # background music
        #               get_wave_object(r'.\audio\music\Arkanoid_SoundTrack_2.wav'),
        #               get_wave_object(r'.\audio\music\Arkanoid_SoundTrack_3.wav')]

        # self.i = 0
        # self.playing_music = self.music[self.i].play()

        self.game = Game()
        self.game.start_game()
        self.__game_field()

    """ Обновление количества очков """

    def __update_score(self):
        self.game.score += 50
        self.canvas.itemconfig(self.text_score, text=f'SCORE: {self.game.score}')

    """ Отрисовка объектов на поле """

    def __game_field(self):
        self.paddle = self.canvas.create_image(self.game.paddle.x,
                                               self.game.paddle.y,
                                               image=self.image_paddle,
                                               anchor='nw')
        self.ball = self.canvas.create_image(self.game.ball.x,
                                             self.game.ball.y,
                                             image=self.image_ball,
                                             anchor='nw')
        for brick in self.game.bricks:
            if not brick.is_invisibility:
                brick.id = self.canvas.create_image(brick.x,
                                                    brick.y,
                                                    image=self.image_bricks[brick.brick_health - 1],
                                                    anchor='nw')

        self.canvas.create_rectangle(0, 480, 520, 600, fill='black')
        self.text_score = self.canvas.create_text(50,
                                                  510,
                                                  font='Arial 20',
                                                  fill='lime',
                                                  anchor='w',
                                                  text=f'SCORE: {self.game.score}')
        self.text_lives = self.canvas.create_text(50,
                                                  560,
                                                  font='Arial 20',
                                                  fill='lime',
                                                  anchor='w',
                                                  text=f'HEALTH: {self.game.lives}')
        self.text_level = self.canvas.create_text(330,
                                                  510,
                                                  font='Arial 20',
                                                  fill='lime',
                                                  anchor='w',
                                                  text=f'LEVEL: {self.game.level_number}')

    """ Обновление координат ракетки до начала и во время игры и мяча до начала игры """

    def __move(self, mouse_x):
        self.game.paddle.move_paddle(mouse_x)
        self.canvas.coords(self.paddle, self.game.paddle.x, self.game.paddle.y)

        if not self.game.is_init_game:
            self.game.ball.move_ball_to_mouse(mouse_x)
            self.canvas.coords(self.ball, self.game.ball.x, self.game.ball.y)

    """ Обновление координат мяча во время игры """

    def __move_ball(self):
        self.game.ball.move_ball()
        self.canvas.coords(self.ball, self.game.ball.x, self.game.ball.y)

    def __check_on_ball_collision_with_brick(self):
        for brick in self.game.bricks:
            if self.ball in self.canvas.find_overlapping(brick.x,
                                                         brick.y,
                                                         brick.x + brick.width_brick,
                                                         brick.y + brick.height_brick):

                # get_wave_object(r'.\audio\sounds\hit_brick.wav').play()  # sound
                if brick.is_invisibility:
                    brick.is_invisibility = False
                else:
                    brick.break_brick(brick, self.game.bricks)
                    self.canvas.delete(brick.id)

                self.game.ball.hit_brick(brick)
                self.__update_score()
                brick.id = self.canvas.create_image(brick.x,
                                                    brick.y,
                                                    image=self.image_bricks[brick.brick_health - 1],
                                                    anchor='nw')
                if brick.brick_health == 0:
                    self.canvas.delete(brick.id)
                break

    def __check_on_ball_collision_with_paddle(self):
        self.__move_ball()
        if self.ball in self.canvas.find_overlapping(self.game.paddle.x,
                                                     self.game.paddle.y,
                                                     self.game.paddle.x + self.game.paddle.width_paddle,
                                                     self.game.paddle.y + self.game.paddle.height_paddle):
            # get_wave_object(r'.\audio\sounds\hit_paddle.wav').play()  # sound

            self.game.ball.hit_paddle(self.game.paddle)
    """
    def __get_music(self):
        if not self.playing_music.is_playing():
            if self.i == len(self.music) - 1:
                self.i = 0
            else:
                self.i += 1
            self.playing_music = self.music[self.i].play()
    """
    def __inform(self, condition, total, s, sound):
        if condition:
            # self.playing_music.stop()  # music
            # get_wave_object(sound).play()  # sound

            if message_box.askyesno(total, f'{s}\nTotal Score: {self.game.score}\nStart again?'):
                self.game = Game()
                self.game.start_game()
                self.canvas.delete(*self.canvas.find_all())
                self.canvas.create_image(0, 0, image=self.image_bg, anchor='nw')
                self.__game_field()
            else:
                quit()

    """ Игра """

    def timer(self):
        # self.__get_music()  # music

        self.__check_on_ball_collision_with_paddle()
        self.__check_on_ball_collision_with_brick()
        self.game.check_on_lose_life()

        self.canvas.itemconfig(self.text_lives, text=f'HEALTH: {self.game.lives}')

        self.__inform(self.game.game_over(), 'Game over', 'You lose!', r'.\audio\sounds\game_over.wav')
        self.__inform(self.game.game_completed(), 'Victory', 'You win!', r'.\audio\sounds\victory.wav')

        if self.game.level_completed():
            # self.playing_music.stop()  # music

            # get_wave_object(r'.\audio\sounds\win.wav').play()  # sound
            message_box.showinfo('', f'Level {self.game.level_number} completed!\nScore: {self.game.score}')

            self.game.level_number += 1
            self.game.start_game()

            if not self.game.game_completed():
                # get_wave_object(r'.\audio\sounds\ready.wav').play()  # sound

                message_box.showinfo('', f'Next level: {self.game.level_number}\nReady? Go!')
                self.canvas.delete(self.paddle, self.ball)
                self.__game_field()

        self.update()
        self.after(10, self.timer)

    def __on_mouse_event(self, event):
        mouse_x = event.x_root - self.winfo_rootx()
        self.__move(mouse_x)

    def __on_mouse_click(self, event):
        self.game.post_click_game()


"""
def get_wave_object(file_name):
    return simpleaudio.WaveObject.from_wave_file(file_name)
"""


def get_image(image_name):
    return Image.open(image_name)


def main():
    form = Form()
    form.timer()
    form.mainloop()


if __name__ == '__main__':
    main()
