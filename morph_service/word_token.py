from sys import intern
from typing import Dict, List


class WordItem:
    def __init__(self, word: str, lemma: str, tag: str, score: float, lexeme: list or None = None):
        self.__word = intern(word)
        self.__lemma = lemma and intern(lemma or '')
        self.__tag = intern(str(tag))
        self.__score = score
        self.__lexeme = lexeme

        try:
            self.__lexeme = [{'word': intern(lx.word), 'lemma': intern(lx.normal_form), 'tag': intern(str(lx.tag))}
                             for lx in lexeme]
        except:
            pass

    @property
    def word(self) -> str:
        return self.__word

    @property
    def lemma(self) -> str:
        return self.__lemma

    @property
    def tag(self) -> str:
        return self.__tag

    @tag.setter
    def tag(self, value: str):
        self.__tag = value

    @property
    def score(self) -> float:
        return self.__score

    @property
    def lexeme(self) -> List[Dict[str, str]]:
        return self.__lexeme

    def __str__(self):
        return f'{self.word} :: {self.tag}'

    def __repr__(self):
        return str(self)

    def as_dict(self) -> dict:
        return {'word': self.word, 'lemma': self.lemma, 'tag': self.tag, 'score': self.score, 'lexeme': self.lexeme}

    @property
    def pos(self) -> str:
        return self.tag.split(',')[0]

    @property
    def base(self):
        return self.word, self.lemma, self.tag

    @base.setter
    def base(self, another: 'WordItem'):
        self.__word, self.__lemma, self.__tag = another.word, another.lemma, another.tag

    @base.deleter
    def base(self):
        self.__word, self.__tag, self.__lemma = '', '', ''
        self.__score = 0
        self.__lexeme = None
