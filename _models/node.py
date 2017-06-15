import _pickle as cPickle
import re
from collections import OrderedDict as oDict
from operator import attrgetter
from typing import List, FrozenSet, Iterator

from cytoolz import pluck, join, identity

from _models.syntax_item import SyntaxItem
from lib_ex.ftools import pluck_attr

RE_STAR = re.compile('\*+')


class Node:
    def __init__(self, word: str):
        self._parsed = {}
        self.__deprel = None
        self._node = None
        self.__is_question = '?' in word

        word = RE_STAR.sub('', word)
        self.__word = word if not self.__is_question else word.replace('?', '')

        self._nf = frozenset()
        self._numbers = frozenset()

    @property
    def word(self) -> str:
        return self.__word

    @property
    def deprel(self) -> str:
        return self.__deprel

    @property
    def is_question(self) -> bool:
        return self.__is_question

    @property
    def node(self) -> str:
        return self._node

    @property
    def lemmas(self) -> FrozenSet[str]:
        return self._nf

    @property
    def numbers(self) -> FrozenSet[int]:
        return self._numbers

    @property
    def parsed(self) -> Iterator[SyntaxItem]:
        return iter(self._parsed.values())

    def take_from_sent(self, sentence: List[SyntaxItem]):
        is_root = False
        for word in sentence:
            if word.word == self.__word:
                self._parsed[word.word] = word
                is_root = word.is_root
                break
        if not is_root:
            try:
                self.__deprel = word.deprel
            except:
                pass
        self._node = word.tag
        self._nf = frozenset([word.lemma])
        self._numbers = frozenset(pluck_attr('number', self.parsed))

        return [list(self.parsed)]

    def fix_with(self, other: 'Node') -> bool:
        if self.__deprel and other.__deprel:
            def check(a: Node, b: Node) -> bool:
                nums_b = b.numbers
                links_a = frozenset(pluck_attr('head', a.parsed))
                if links_a & nums_b:
                    b.__deprel = None
                    return True
                return bool(b.deprel)

            if check(self, other) or check(other, self):
                return True
            self.__deprel = other.__deprel = None
            return False
        if self.__deprel or other.__deprel:
            def check_one(a: Node, b: Node) -> bool:
                if not {x.head for x in a.parsed} & b.numbers:
                    self.__deprel = None
                return bool(self.deprel)

            return check_one(self, other) or check_one(other, self)
        return False

    def check_links(self, other: 'Node') -> bool:
        if self.__deprel or other.__deprel:
            def check_one(a: Node, b: Node) -> bool:
                return bool({x.head for x in a.parsed} & b.numbers)

            return check_one(self, other) or check_one(other, self)
        return False

    def is_links_to(self, other: 'Node') -> bool:
        return self.check_links(other)

    def __str__(self):
        return self.__word

    def __repr__(self):
        return str(self)

    @staticmethod
    def select_word(word: str) -> 'Node':
        return Node(word) if '_' not in word else MultiNode(word)

    def __deepcopy__(self, memodict={}):
        return cPickle.loads(cPickle.dumps(self, -1))


class MultiNode(Node):
    def __init__(self, words: str):
        super().__init__(words)
        self._parsed = oDict()
        words = RE_STAR.sub('', words)
        self.__words = words.split('_') if not self.is_question else words.replace('?', '').split('_')

    def take_from_sent(self, sentence: List[SyntaxItem]):
        is_root = False
        for word in pluck(1, join(identity, self.__words, attrgetter('word'), sentence)):
            self._parsed[word.word] = word
            is_root |= word.is_root
        if not is_root:
            nums = frozenset(map(attrgetter('number'), self.parsed)) | {-1}
            links = list(filter(lambda it: it.head not in nums, self.parsed))
            if len(links) == 1:
                self.__deprel = links[0].deprel

        self._node = '|'.join(t.tag for t in self.parsed)
        self._nf = frozenset(t.lemma for t in self.parsed)
        self._numbers = frozenset(pluck_attr('number', self.parsed))

        return [list(self.parsed)]
