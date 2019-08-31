import numpy as np
import pytest

from .main import Object


class TestObject():
    def test_initialization(self):
        # not numpy array
        with pytest.raises(Exception) as e:
            array = 2
            obj = Object(array, (0, 0, 0))

        # wrong shapes
        with pytest.raises(Exception) as e:
            array = np.ones((3, 3))
            obj = Object(array, (0, 0, 0))
        with pytest.raises(Exception) as e:
            array = np.ones((3, 3, 2))
            obj = Object(array, (0, 0, 0))
        with pytest.raises(Exception) as e:
            array = np.ones((3, 3, 5))
            obj = Object(array, (0, 0, 0))

        # right shape
        array = np.ones((3, 3, 3))
        obj = Object(array, (0, 0, 0))

        array = np.ones((4, 4, 4))
        self.obj = Object(array, (0, 0, 0))

    def test_color_changing(self):
        array = np.array([[[34, 42, 3, 1], [22, 33, 3, 0]]])
        obj = Object(array, (0, 0, 0))
        assert np.all(obj.image == np.array([[[34, 42,  3,  1], [22, 33,  3,  0]]]))
        obj.change_color(new_color=(0, 0, 0), old_color=(34, 42, 3))
        assert np.all(obj.image == np.array([[[0,  0,  0,  1], [22, 33,  3,  0]]]))
