import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
import os

from random import randint
from io import BytesIO


class World():
    def __init__(self, dimension=2):
        self.disable_jupyter_notebook_mode()

    def enable_jupyter_notebook_mode(self):
        import IPython as IPython
        self._IPython = IPython
        self._notebook = True

    def disable_jupyter_notebook_mode(self):
        self._notebook = False

    def create_an_image(self, width=1920, height=1080, background_color=(255, 255, 255), existing_picture=None):
        if isinstance(existing_picture, np.ndarray):
            image = np.zeros(
                (existing_picture.shape[0], existing_picture.shape[1], 3), dtype=np.uint8)
        else:
            image = np.zeros((height, width, 3), dtype=np.uint8)
        image[:, :] = background_color
        self.image = image

    def get_random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

    def draw_a_point(self, x, y, color=(0, 0, 0)):
        self.image[y][x] = color

    def show(self):
        if self._notebook:
            # self._IPython.display.clear_output()
            #f = BytesIO()
            # Image.fromarray(self.image).save(f, 'png') #jpeg
            # self._IPython.display.display(self._IPython.display.Image(data=f.getvalue()))
            plt.figure(num='numpy world')
            plt.imshow(self.image)
            figManager = plt.get_current_fig_manager()
            figManager.full_screen_toggle()
            plt.show(block=False)
            plt.pause(2)
            plt.close()
        else:
            image = Image.fromarray(self.image)
            image.show(title="numpy world")

    def save(self, target_file_path="temp.png"):
        Image.fromarray(self.image).convert("RGB").save(target_file_path)

    def show_animation(self, a_function_which_returns_an_image_according_to_a_time_variable, duration=3, fps=24, saving_path=None):
        """
        the function looks like `func(t)`.
        t is a float variable in seconds, for example, 1.2 = 1 second + 0.2 second
        """
        animation = VideoClip(
            a_function_which_returns_an_image_according_to_a_time_variable, duration=duration)
        if self._notebook:
            result = animation.ipython_display(
                fps=fps, loop=True, autoplay=True)
            self._IPython.display.display(result)
        else:
            animation.preview(fps=fps)

        if saving_path != None:
            if len(saving_path.split(".")) > 0:
                extension = saving_path.split(".")[-1]
                if extension.lower() == "gif":
                    animation.write_gif(saving_path, fps=fps)
                elif extension.lower() == "mp4":
                    animation.write_videofile(saving_path, fps=fps)
                else:
                    print("you can only save gif or mp4!")
                    exit()


if __name__ == "__main__":
    width = 1920
    height = 1080

    world = World()
    world.create_an_image(width=width, height=height)
    world.disable_jupyter_notebook_mode()

    for x in range(width):
        for y in range(height):
            if width/7 * 1 < x < width / 7 * 2:
                world.draw_a_point(x, y, (0, 255, 0))
            if width/7 * 3 < x < width / 7 * 4:
                world.draw_a_point(x, y, (0, 0, 0))
            if width/7 * 5 < x < width / 7 * 6:
                world.draw_a_point(x, y, (255, 0, 0))

    world.show()
