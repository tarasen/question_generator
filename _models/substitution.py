from functools import lru_cache
from typing import FrozenSet, List


class Substitution:
    def __init__(self, numbers: FrozenSet[int], lemmas: FrozenSet[str], tag: str):
        self.__numbers = numbers
        self.__lemmas = lemmas
        self.__tag = tag.replace('intr', 'tran')
        self.__hash = (','.join(map(str, numbers)) + '|'.join(lemmas) + '|' + tag).__hash__()
        self.__is_question = '?' in self.tag
        self.__tags = tag.split('|')

    @property
    def numbers(self) -> FrozenSet[int]:
        return self.__numbers

    @property
    def lemmas(self) -> FrozenSet[str]:
        return self.__lemmas

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def tags(self) -> List[str]:
        return self.__tags

    @property
    def is_question(self) -> bool:
        return self.__is_question

    def __eq__(self, other):
        return self.__hash == other.__hash

    def __hash__(self):
        return self.__hash

    def __str__(self):
        return str((self.numbers, self.lemmas, self.tag))

    def __repr__(self):
        return str(self)