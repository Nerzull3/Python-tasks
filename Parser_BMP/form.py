import glob
import os
import tkinter
from collections import OrderedDict

from parser_bitmap import ParserBMP


class Form(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.width = tkinter.Tk.winfo_screenwidth(self) - 100
        self.height = tkinter.Tk.winfo_screenheight(self) - 100
        self.geometry(str(self.width) + 'x' + str(self.height))
        self.resizable(width=False, height=False)
        self.canvas = tkinter.Canvas(self, width=self.width, height=self.height)

        os.chdir('pictures')
        self.bmp_paths = glob.glob('*.bmp')
        self.index = 0

        self.update()
        self.canvas.pack()

    def update(self):
        self.canvas.delete(*self.canvas.find_all())
        self.__get_buttons()
        self.parser = ParserBMP(self.bmp_paths[self.index])
        self.data = OrderedDict(self.parser.get_data_about_bmp())
        self.__draw_information()
        self.__draw_picture()

    def __get_buttons(self):
        self.button_left = tkinter.Button(text="<", command=self.__get_previous_photo)
        self.button_left.place(x=70, y=self.height - 50, width=50, height=50)
        if self.index - 1 < 0:
            self.button_left.config(state='disabled')

        self.button_right = tkinter.Button(text=">", command=self.__get_next_photo)
        self.button_right.place(x=120, y=self.height - 50, width=50, height=50)
        if self.index + 1 >= len(self.bmp_paths):
            self.button_right.config(state='disabled')

    def __get_next_photo(self):
        self.button_right.config(state='active')
        self.index += 1
        print('Next photo!')
        self.update()

    def __get_previous_photo(self):
        self.button_left.config(state='active')
        self.index -= 1
        print('Previous photo!')
        self.update()

    def __draw_information(self):
        y = 0
        for key, value in self.data.items():
            self.canvas.create_text(
                self.width - 600,
                50 + y,
                font='Arial 12',
                anchor='w',
                text=key + ': ' + str(value)
            )
            print(key + ': ' + str(value))
            y += 25

    def __draw_picture(self):
        image_w = self.data['Width']
        image_h = self.data['Height']
        self.image = tkinter.PhotoImage(width=image_w, height=image_h)
        info_image = self.parser.get_bytes_image(self.bmp_paths[self.index])

        depth = self.data['Count bits']
        if depth == 32:
            colors = [[info_image[i + j] for i in range(2, -1, -1)] for j in range(0, len(info_image) - 4, 4)]
        elif depth == 24:
            colors = [[info_image[i + j] for i in range(2, -1, -1)] for j in range(0, len(info_image) - 3, 3)]
        elif depth == 16:
            colors = [[info_image[i + j] for i in range(2, -1, -1)] for j in range(0, len(info_image) - 2, 2)]
        elif depth == 8:
            colors = [[info_image[j] for _ in range(3)] for j in range(len(info_image))]
        else:
            colors = [[info_image[i + j] for i in range(2, -1, -1)] for j in range(0, len(info_image) - 3, 3)]

        x, y = 0, image_h - 1
        for color in colors:
            pixel = '#%02x%02x%02x' % (color[0], color[1], color[2])
            self.image.put(pixel, (x, y))
            x += 1
            if x == image_w:
                y -= 1
                x = 0

        self.canvas.create_image(
            10,
            10,
            image=self.image,
            anchor='nw'
        )


def main():
    form = Form()
    form.mainloop()


if __name__ == '__main__':
    main()
