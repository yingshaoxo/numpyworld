import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from moviepy.editor import VideoClip
import os

from random import randint
from io import BytesIO


class Object():
    def __init__(self, numpy_array, color=(0, 0, 0)):
        assert isinstance(numpy_array, np.ndarray), "The first argument of Object() should be an numpy_array"

        shape = numpy_array.shape
        assert len(shape) == 3 and shape[2] in [1, 3, 4], f"The shape of that numpy_array should be (*, *, 1 or 3 or 4), but you gave me {shape}"

        numpy_array = numpy_array.astype(int)

        """
        numpy.where(condition[, x, y])
        condition : array_like, bool, Where True, yield x, otherwise yield y.
        """

        # just a point squre which shows the object shape, we assume it just have one specify color
        if shape[2] == 1:
            self._raw_data = numpy_array
            self._color = color
            self.image = np.where(numpy_array == 1, [color[0], color[1], color[2], 255], [0, 0, 0, 0])
        # rgb array, like the format of jpg
        elif shape[2] == 3:
            self._raw_data = None
            self._color = None
            self.image = np.insert(numpy_array, 3, 255, axis=2)

        # rgba array, like the format of png
        elif shape[2] == 4:
            self._raw_data = None
            self._color = None
            self.image = numpy_array

    def change_color(self, new_color, old_color=None):
        if old_color == None:
            assert self._color != None, "you have to tell me the old_color for changing the color of this object"
            old_color = self._color

        old_color = list(old_color)
        old_color.append(255)
        new_color = list(new_color)
        new_color.append(255)

        mask = np.all(self.image[:, :, 0:4] == old_color, axis=2)
        self.image[mask] = new_color


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

        # add an alpha layer for transparency
        image = np.insert(image, 3, 255, axis=2)
        self.image = image

    def get_random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

    def draw_a_point(self, x, y, color=(0, 0, 0)):
        self.image[y][x] = (color[0], color[1], color[2], 255)

    def draw(self, object_image, left_top_position=(0, 0)):
        assert isinstance(object_image, np.ndarray), "the object_image paramater must be an numpy array"

        object_shape = object_image.shape
        assert len(object_shape) == 3 and object_shape[2] == 4, f"The shape of that numpy_array should be (*, *, 4), but you gave me {shape}"
        h, w, _ = object_shape

        assert len(left_top_position) == 2, "left_top_position should be (x, y)"
        x, y = left_top_position

        #print(self.image[y:y+h, x:x+w]==[-1, -1, -1, 255])
        #self.image[y:y+h, x:x+w] = np.where(self.image[y:y+h, x:x+w]==[-1, -1, -1, 255], object_image, self.image[y:y+h, x:x+w])
        self.image[y:y+h, x:x+w] = object_image

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

    def save(self, target_file_path="__temp__.png"):
        Image.fromarray(self.image).convert("RGBA").save(target_file_path)

    def show_animation(self, a_function_which_returns_an_image_according_to_a_time_variable, duration=3, fps=24, saving_path=None):
        """
        the function looks like `func(t)`.
        t is a float variable in seconds, for example, 1.2 = 1 second + 0.2 second
        """
        def wrap_function(t):
            array = a_function_which_returns_an_image_according_to_a_time_variable(t)
            assert isinstance(array, np.ndarray), "this function should return an numpy array"
            if array.shape[2] == 4:
                array = array[:, :, 0:3]

            return array

        animation = VideoClip(wrap_function, duration=duration)
        if self._notebook:
            result = animation.ipython_display(fps=fps, loop=True, autoplay=True)
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
