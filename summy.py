# -*- coding: utf-8 -*-

import re

from nltk import word_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.utils import get_stop_words

from _web_clients.morph_client import MorphClient

__all__ = ['Summarizer']


class RussianStimmer:
    def __init__(self, mc: MorphClient):
        self.mc = mc

    def __call__(self, *args, **kwargs):
        word = args[0]
        return self.mc.parse_one(word)[0].lemma


class RussianTokenizer:
    def __init__(self):
        self.RE_SENT = re.compile('(?<!\w\.\w.)(?<![A-ZА-ЯЁ][a-zа-яё]\.)(?<=[.?!])\s')
        self.RE_WORD = re.compile(r"^[^\W\d_]+$")

    def to_sentences(self, paragraph):
        return tuple(map(str.strip, self.RE_SENT.split(paragraph)))

    def to_words(self, sentence):
        words = word_tokenize(sentence)
        return tuple(filter(self._is_word, words))

    def _is_word(self, word):
        return bool(self.RE_WORD.match(word))


class Summarizer:
    def __init__(self, mc: MorphClient):
        self.__summarizer = LexRankSummarizer(RussianStimmer(mc))
        self.__summarizer.stop_words = get_stop_words("russian")

        self.__tokenizer = RussianTokenizer()

    def get_summary(self, text: str, pers: int or float):
        parser = PlaintextParser.from_string(text, self.__tokenizer)
        size = int(len(parser.document.sentences) * pers) if 0 < pers < 1 else pers
        return map(str, self.__summarizer(parser.document, size))


if __name__ == "__main__":
    TEXT = """
    Выделение главных мыслей в виде реферата или конспекта интересовало человечество со времен появления письменности. С появлением Интернета тема приобрела новую актуальность, так как нынешние объемы информации огромны и постоянно растут. Существует множество областей, в которых применение такого сокращенного представления давало бы существенный выигрыш. Например, система может быть полезна для человека, который должен по большому количеству статьей на определенную тему быстро получить представление о данной области. Автоматическое реферирование также можно использовать в поисковых системах для того, чтобы уменьшать область поиска. Рефераты бывают нескольких типов: информативные, индикативные и критические. Индикативные рефераты должны предоставлять достаточно информации для принятия решения, стоит ли обращаться к оригиналу. Информативные рефераты должны сжимать исходный текст. Критические рефераты не только сокращают, но и дают оценку тексту. В данной системе будут рассматриваться только рефераты информативного типа. Существует два основных подхода к автоматическому реферированию. Первый подход ориентирован на извлечение важных фрагментов, обычно предложений, так называемый sentenceextraction. Второй подход использует сложные методы семантического и лингвистического анализа, обычно это генерация рефератов (summarygeneration) на основе семантического представления текста. Ввиду сложности второго подхода, как в плане реализации, так и в плане вычислений, а также потому, что он накладывает существенные ограничения на тексты, было принято основывать свою систему на первом подходе. Разработанная система организована в виде веб-сервиса, позволяющего: определять язык, получить ключевые слова из текста, выделить в тексте основные предложения, создавать реферат состоящий из основных предложении. Указывать алгоритм реферирования, а также длину получаемого реферата. Все алгоритмы должны корректно работать с несколькими языками. 
    """

    mc = MorphClient()
    smr = Summarizer(mc)

    print('\n'.join(smr.get_summary(TEXT, 0.4)))
