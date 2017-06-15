import re
from typing import List

from nltk import word_tokenize

__all__ = ['Tokenizer']

RE_THREE_DOT = re.compile("…")
RE_QUOTES = re.compile("[«»“„”]")
RE_DEFIS = re.compile("–|(---?)")

class Tokenizer:
    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        return list(map(str.lower, word_tokenize(text)))

    @classmethod
    def fix_text(cls, text: str) -> str:
        text = RE_THREE_DOT.sub("...", text)
        text = RE_QUOTES.sub('"', text)
        return RE_DEFIS.sub("-", text)
