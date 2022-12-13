"""Generic utilities."""
import re
from typing import Any, List, Sequence, Tuple


def strip_punctuation(text: str) -> str:
    """Strip punctuation from the string."""
    return re.sub(r"\p{P}+", " ", text)


def strip_whitespace(text: str) -> str:
    """Strip all whitespace from the string."""
    return re.sub(r"\s+", "", text)


def find_sublist(l: Sequence[Any], sublist: Sequence[Any]) -> int:
    """Return the index of the first occurrence of sublist in l.

    Args:
        l: the list to search for the sublist.
        sublist: the sublist.

    Returns:
        The index of the first occurrence of sublist in l.
        If the sublist is not found, return -1.
    """
    for i in range(len(l)):
        # Check index 0 first for optimization
        if l[i] == sublist[0] and l[i : i + len(sublist)] == sublist:
            return i
    return -1


class Phrase:
    """Represents a string and its tokenization.

    Uses regex-based tokenization copied from nltk.tokenize.RegexpTokenizer.
    Tokenization is computed lazily.
    """

    # I like "trains". --> [I, like, ", trains, ", .]
    TOKENIZER = re.compile(r"\w+|[^\w\s]", re.UNICODE | re.MULTILINE | re.DOTALL)

    def __init__(self, text: str):
        """Initialize a Phrase.

        Args:
            text: the string content.
        """
        self._text = str(text)
        self._tokens = None

    @property
    def text(self) -> str:
        """Return the string content."""
        return self._text

    def _tokenize(self):
        tokens: List[str] = []
        token_spans: List[Tuple[int, int]] = []
        for m in self.TOKENIZER.finditer(self._text):
            tokens.append(m.group())
            token_spans.append(m.span())
        self._tokens = tuple(tokens)
        self._token_spans = tuple(token_spans)

    @property
    def tokens(self) -> Sequence[str]:
        """Return the tokens."""
        if self._tokens is None:
            self._tokenize()
        assert self._tokens is not None
        return self._tokens

    def detokenize(self, start: int, end: int) -> str:
        """Return the substring corresponding to tokens[start:end].

        Args:
            start: start token index (inclusive)
            end: end token index (exclusive)

        Returns:
            The substring corresponding to tokens[start:end]
        """
        if self._tokens is None:
            self._tokenize()
        return self._text[self._token_spans[start][0] : self._token_spans[end - 1][1]]

    def __repr__(self) -> str:
        """Return __repr__ of the string."""
        return repr(self._text)

    def __str__(self):
        """Return __str__ of the string."""
        return str(self._text)


def word_tokenize(text: str) -> Sequence[str]:
    """Tokenize the string without keeping the mapping to the original string."""
    return Phrase.TOKENIZER.findall(text)
