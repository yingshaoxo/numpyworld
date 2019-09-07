# Numpy World

Draw this world with numpy.  

> We firmly believe once you can draw one picture with programming, you can also draw a series of that kind of pictures with programming too.

### Installation

```
sudo pip3 install numpyworld
```

### Usage

```python
from numpyworld import World

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
```

### More

[Jupyter-notebook Examples](https://github.com/yingshaoxo/numpyworld/blob/master/Example.ipynb)
