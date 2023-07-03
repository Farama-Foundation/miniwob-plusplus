"""Test the custom spaces."""
import numpy as np
from gymnasium.spaces import Box, Text
from gymnasium.spaces.utils import flatdim, flatten, flatten_space, unflatten

from miniwob.spaces import Unicode


class TestUnicode:
    """Test the Unicode space."""

    def test_unicode_contains(self):
        """Test the `contains` method."""
        space = Unicode(20, min_length=4, charset="abc")
        assert space.contains("Hello, World!")
        assert space.contains("Привет мир!")
        assert space.contains("This has 20 letters.")
        assert not space.contains("This is longer than 20 letters.")
        assert not space.contains("cab")

    def test_unicode_sample(self):
        """Test the `sample` method."""
        space = Unicode(20, min_length=4, charset="abc")
        for _ in range(5):
            x = space.sample()
            assert all(char in "abc" for char in x)
            assert 4 <= len(x) <= 20

    def test_unicode_flatten(self):
        """Test the flatten utilities for Unicode."""
        space = Unicode(10, min_length=4, charset="abc")
        assert flatdim(space) == 10
        flattened_space = flatten_space(space)
        assert isinstance(flattened_space, Box)
        x = "你好世界"
        flattened_x = flatten(space, x)
        assert np.all(flattened_x == np.array([20320, 22909, 19990, 30028] + [0] * 6))
        assert x == unflatten(space, flattened_x)

    def test_text_flatten(self):
        """Test that the space utilities still work with Text."""
        space = Text(10, min_length=4, charset="abc")
        assert not space.contains("Hello, world!")
        assert flatdim(space) == 10
        flattened_space = flatten_space(space)
        assert isinstance(flattened_space, Box)
        x = "baca"
        flattened_x = flatten(space, x)
        assert np.all(flattened_x == np.array([1, 0, 2, 0] + [3] * 6))
        assert x == unflatten(space, flattened_x)
