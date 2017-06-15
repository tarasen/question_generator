from sys import intern
from typing import List

import pymorphy2
from cytoolz import memoize

from morph_service.word_token import WordItem


class FrequencyAlg(object):
    morph = pymorphy2.MorphAnalyzer()

    @staticmethod
    @memoize()
    def morphy(word: str, lexeme: bool = False) -> List[WordItem]:
        return [
            WordItem(intern(parsed.word), intern(parsed.normal_form), intern(str(parsed.tag)), parsed.score,
                     parsed.lexeme if lexeme else None)
            for parsed in FrequencyAlg.morph.parse(word)]

    def morph_one(self, word: str) -> WordItem:
        return self.morphy(word)[0]

    def parse_sentence(self, words: List[str]) -> List[WordItem]:
        return list(map(self.morph_one, words))


if __name__ == "__main__":
    from pprint import pprint

    m = FrequencyAlg()
    pars = m.morphy('мыла', True)
    pprint([p.as_dict() for p in pars])
