import _pickle as cPickle

from morph_service.word_token import WordItem


class SyntaxItem(WordItem):
    def __init__(self, number: int, word: str, lemma: str, tag: str, score: float, head: int, deprel: str):
        super().__init__(word, lemma, tag, score)
        self.__number = number
        self.__head = head
        self.__deprel = deprel
        self.__is_root = head == -1 and deprel in ['root', 'ROOT']
        self.__link = None
        self.__children = []

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value: int):
        self.__number = value

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, value: int):
        self.__is_root = value == -1 and self.__deprel in ['root', 'ROOT']
        self.__head = value

    @property
    def deprel(self):
        return self.__deprel

    @deprel.setter
    def deprel(self, value: str):
        self.__is_root = self.__head == -1 and value in ['root', 'ROOT']
        self.__deprel = value

    @property
    def is_root(self):
        return self.__is_root

    @property
    def link(self):
        return self.__link

    def set_link(self, another_word: 'SyntaxItem'):
        self.__link = another_word
        another_word.__children.append(self)

    def clear_syntax(self):
        self.__link = None
        self.__children = []

    def fix_syntax(self, another: 'SyntaxItem'):
        self.__number, self.__head, self.__deprel = another.number, another.head, another.deprel

        self.__is_root = self.head == -1 and self.deprel in ['root', 'ROOT']
        self.__link = None
        self.__children = []

    def __deepcopy__(self, memodict={}):
        return cPickle.loads(cPickle.dumps(self, -1))
