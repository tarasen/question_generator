import _pickle as cPickle
from typing import List

from _models.syntax_item import SyntaxItem
from lib_ex.ftools import pluck_attr
from morph_service.word_token import WordItem


class DummySentence:
    def __init__(self, words: List[WordItem]):
        self._words = words

    def __copy__(self):
        return self._words.copy()

    @property
    def original(self):
        return ' '.join(pluck_attr('word', self))

    def __str__(self):
        return self.original

    def __repr__(self):
        return str(self)

    def __getitem__(self, item):
        return self._words[item]

    def __len__(self):
        return len(self._words)

    def __iter__(self):
        return iter(self._words)

    def __deepcopy__(self, memodict={}):
        return cPickle.loads(cPickle.dumps(self, -1))

    def __delitem__(self, key):
        self._words.remove(key)

    def __hash__(self):
        return self.original.__hash__()

    def __eq__(self, other: 'Sentence'):
        return self.original == other.original

    def insert(self, frm: int, to: int, rul: List[SyntaxItem]):
        self._words[frm:to] = rul


class Sentence(DummySentence):
    def __init__(self, words: List[SyntaxItem]):
        super().__init__(words)
        self.init_links()

    def init_links(self):
        for w in self:
            w.clear_syntax()

        for w in self:
            if w.head != -1:
                w.set_link(next(rw for rw in self if w.head == rw.number))

    @property
    def key(self):
        return tuple((w.tag, w.head, w.deprel) for w in self)
