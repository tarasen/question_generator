from functools import lru_cache
from typing import Set, Tuple, FrozenSet

from _models.node import Node
from _models.syntax_item import SyntaxItem


class Transform:
    def __init__(self, a: Node, b: Node, variants: Set[Tuple[str, str]]):
        self.__node_a = a
        self.__node_b = b
        self.__variants = frozenset(variants)

        self.__lemmas = None
        self.__numbers = None

    @property
    def node_a(self) -> Node:
        return self.__node_a

    @property
    def node_b(self) -> Node:
        return self.__node_b

    @property
    def numbers(self) -> FrozenSet[int]:
        if self.__numbers is None:
            self.__numbers = self.node_a.numbers | self.node_b.numbers
        return self.__numbers

    @property
    def lemmas(self) -> FrozenSet[str]:
        if self.__lemmas is None:
            self.__lemmas = frozenset(self.node_a.lemmas | self.node_b.lemmas)
        return self.__lemmas

    @property
    def parsed_a(self) -> Tuple[SyntaxItem, ...]:
        return tuple(self.node_a.parsed)

    @property
    def parsed_b(self) -> Tuple[SyntaxItem, ...]:
        return tuple(self.node_b.parsed)

    @property
    def variants(self) -> FrozenSet[Tuple[str, str]]:
        return self.__variants

    @property
    def key(self) -> Tuple[str, str]:
        return self.node_a.word, self.node_b.word

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self)
