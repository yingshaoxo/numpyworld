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

        """
        numpy.where(condition[, x, y])
        condition : array_like, bool, Where True, yield x, otherwise yield y.
        """

        # just a point squre which shows the object shape, we assume it just have one specify color
        if shape[2] == 1:
            self._raw_data = numpy_array
            self._color = color
            if len(color) == 3:
                self.image = np.where(numpy_array == 1, [color[0], color[1], color[2], 255], [0, 0, 0, 0]).astype(np.uint8)
            elif len(color) == 4:
                self.image = np.where(numpy_array == 1, [color[0], color[1], color[2], color[3]], [0, 0, 0, 0]).astype(np.uint8)
        # rgb array, like the format of jpg
        elif shape[2] == 3:
            self._raw_data = None
            self._color = None
            self.image = np.insert(numpy_array, 3, 255, axis=2).astype(np.uint8)

        # rgba array, like the format of png
        elif shape[2] == 4:
            self._raw_data = None
            self._color = None
            self.image = numpy_array.astype(np.uint8)

        self.disable_jupyter_notebook_mode()
        self._backup_images = {}

    def enable_jupyter_notebook_mode(self):
        import IPython as IPython
        self._IPython = IPython
        self._notebook = True

    def disable_jupyter_notebook_mode(self):
        self._notebook = False

    def create_an_object(self, numpy_array, color=(0, 0, 0)):
        return Object(numpy_array, color=color)

    def backup(self, key="default"):
        assert isinstance(key, str), "key must be a string"
        self._backup_images.update({key: self.image.copy()})

    def restore(self, key="default"):
        assert isinstance(key, str), "key must be a string"
        if len(self._backup_images) != 0:
            result = self._backup_images.get(key)
            if isinstance(result, np.ndarray):
                self.image = result.copy()

    def get_random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

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

        self._color = tuple(new_color[:3])

    def draw_a_point(self, x, y, color=(0, 0, 0)):
        if len(color) == 3:
            self.image[y][x] = (color[0], color[1], color[2], 255)
        elif len(color) == 4:
            self.image[y][x] = (color[0], color[1], color[2], color[3])

    def draw(self, object_image, left_top_position=(0, 0), center_position=None):
        # if isinstance(object_image, Object):
        #    object_image = object_image.image
        assert isinstance(object_image, np.ndarray), "the first paramater must be an numpy array, try to give `object.image` as the paramater"

        object_shape = object_image.shape
        assert len(object_shape) == 3 and object_shape[2] == 4, f"The shape of that numpy_array should be (*, *, 4), but you gave me {shape}"
        h, w, _ = object_shape

        if center_position != None:
            assert len(center_position) == 2, "center_position must be (x,y)"
            left_top_x = center_position[0] - w/2
            left_top_y = center_position[1] - h/2
            left_top_position = (int(left_top_x), int(left_top_y))

        assert len(left_top_position) == 2, "left_top_position should be positive (x, y)"

        backgound_Image = Image.fromarray(self.image, mode="RGBA")
        object_Image = Image.fromarray(object_image, mode="RGBA")
        backgound_Image.paste(object_Image, box=left_top_position, mask=object_Image)

        self.image = np.array(backgound_Image).astype(np.uint8)

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


class World(Object):
    def __init__(self, width=1920, height=1080, background_color=(255, 255, 255), existing_picture=None):
        numpy_array = self._create_an_image(width, height, background_color, existing_picture)
        super().__init__(numpy_array)

    def _create_an_image(self, width=1920, height=1080, background_color=(255, 255, 255), existing_picture=None):
        if isinstance(existing_picture, np.ndarray):
            image = np.zeros(
                (existing_picture.shape[0], existing_picture.shape[1], 3), dtype=np.uint8)
        else:
            image = np.zeros((height, width, 3), dtype=np.uint8)

        assert 3 <= len(background_color) <= 4, "the background_color is something like RGB(255, 255, 255) or RGBA(0,0,0,0)"
        image[:, :] = list(background_color)[:3]

        # add an alpha layer for transparency
        if len(background_color) == 3:
            image = np.insert(image, 3, 255, axis=2).astype(np.uint8)
        elif len(background_color) == 4:
            image = np.insert(image, 3, background_color[3], axis=2).astype(np.uint8)

        return image

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

    world = World(width=width, height=height)
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
