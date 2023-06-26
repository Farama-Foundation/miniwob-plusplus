"""Custom spaces for MiniWoB++."""
from __future__ import annotations

from typing import Any

import numpy as np
from gymnasium.spaces import Box
from gymnasium.spaces.space import Space
from gymnasium.spaces.text import alphanumeric
from gymnasium.spaces.utils import flatdim, flatten, flatten_space, unflatten
from numpy.typing import NDArray


MAX_UNICODE_CODEPOINT = 0x10FFFF


class Unicode(Space[str]):
    """A space representing a unicode string.

    Unicode is a replacement for the Text space in Gymnasium, with the
    following differences:

    - Each character can be an arbitrary unicode character.
    - The sample method samples from the specified character set.
    """

    def __init__(
        self,
        max_length: int,
        *,
        min_length: int = 1,
        sample_charset: frozenset[str] | str = alphanumeric,
        seed: int | np.random.Generator | None = None,
    ):
        """Constructor for the `Unicode` space.

        Args:
            max_length: Maximum text length (in characters).
            min_length: Minimum text length (in characters). Defaults to 1.
            sample_charset: Character set for sampling from the space.
            seed: The seed for sampling from the space.
        """
        self.min_length: int = int(min_length)
        self.max_length: int = int(max_length)
        self._sample_charlist: tuple[str, ...] = tuple(sample_charset)
        super().__init__(dtype=str, seed=seed)

    def sample(
        self,
        mask: None | Any = None,
    ):
        """Generates a single random sample from this space."""
        if mask is not None:
            assert isinstance(
                mask, tuple
            ), f"Expects the mask type to be a tuple, actual type: {type(mask)}"
            assert (
                len(mask) == 2
            ), f"Expects the mask length to be two, actual length: {len(mask)}"
            length, charlist_mask = mask

            if length is not None:
                assert np.issubdtype(
                    type(length), np.integer
                ), f"Expects the Text sample length to be an integer, actual type: {type(length)}"
                assert (
                    self.min_length <= length <= self.max_length
                ), f"Expects the Text sample length be between {self.min_length} and {self.max_length}, actual length: {length}"

            if charlist_mask is not None:
                assert isinstance(
                    charlist_mask, np.ndarray
                ), f"Expects the Text sample mask to be an np.ndarray, actual type: {type(charlist_mask)}"
                assert (
                    charlist_mask.dtype == np.int8
                ), f"Expects the Text sample mask to be an np.ndarray, actual dtype: {charlist_mask.dtype}"
                assert charlist_mask.shape == (
                    len(self._sample_charlist),
                ), f"expects the Text sample mask to be {(len(self._sample_charlist),)}, actual shape: {charlist_mask.shape}"
                assert np.all(
                    np.logical_or(charlist_mask == 0, charlist_mask == 1)
                ), f"Expects all masks values to 0 or 1, actual values: {charlist_mask}"
        else:
            length, charlist_mask = None, None

        if length is None:
            length = self.np_random.integers(self.min_length, self.max_length + 1)

        if charlist_mask is None:
            string = self.np_random.choice(self._sample_charlist, size=length)
        else:
            valid_mask = charlist_mask == 1
            valid_indexes = np.where(valid_mask)[0]
            if len(valid_indexes) == 0:
                if self.min_length == 0:
                    string = ""
                else:
                    # Otherwise the string will not be contained in the space
                    raise ValueError(
                        f"Trying to sample with a minimum length > 0 ({self.min_length}) but the character mask is all zero meaning that no character could be sampled."
                    )
            else:
                string = "".join(
                    self._sample_charlist[index]
                    for index in self.np_random.choice(valid_indexes, size=length)
                )

        return "".join(string)

    def contains(self, x: Any) -> bool:
        """Return boolean specifying if x is a valid member of this space."""
        return isinstance(x, str) and self.min_length <= len(x) <= self.max_length

    def __repr__(self) -> str:
        """Gives a string representation of this space."""
        return f"Unicode({self.min_length}, {self.max_length})"

    def __eq__(self, other: Any) -> bool:
        """Check whether ``other`` is equivalent to this instance."""
        return (
            isinstance(other, Unicode)
            and self.min_length == other.min_length
            and self.max_length == other.max_length
        )

    @property
    def is_np_flattenable(self) -> bool:
        """The flattened version is the array of unicode codepoints, padded with 0 to the max character length."""
        return True


@flatdim.register(Unicode)
def _flatdim_unicode(space: Unicode) -> int:
    return space.max_length


@flatten.register(Unicode)
def _flatten_unicode(space: Unicode, x: str) -> NDArray[np.int32]:
    arr = np.full(shape=(space.max_length,), fill_value=0, dtype=np.int32)
    for i, val in enumerate(x):
        arr[i] = ord(val)
    return arr


@unflatten.register(Unicode)
def _unflatten_unicode(space: Unicode, x: NDArray[np.int32]) -> str:
    return "".join(chr(val) for val in x if val)


@flatten_space.register(Unicode)
def _flatten_space_unicode(space: Unicode) -> Box:
    return Box(
        low=0, high=MAX_UNICODE_CODEPOINT, shape=(space.max_length,), dtype=np.int32
    )
