import numpy as np
import pytest

try:
    from .main import Object
except Exception as e:
    print(e)
    from main import Object


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
        array = np.array([[[255, 0, 0, 255], [0, 255, 0, 255]]])
        obj = Object(array, (0, 0, 0))
        assert np.all(obj.image == np.array([[[255, 0, 0, 255], [0, 255, 0, 255]]]))
        obj.change_color(new_color=(0, 0, 255), old_color=(255, 0, 0))
        assert np.all(obj.image == np.array([[[0, 0, 255, 255], [0, 255, 0, 255]]]))


if __name__ == "__main__":
    pass
