from functools import reduce, lru_cache
from operator import add as plus
from typing import List

import russian_tagsets
from cytoolz import cons


class CONLLUConverter:
    def __init__(self):
        self.converter = russian_tagsets.ud.to_ud20

    @lru_cache(maxsize=256)
    def _convert_to_ud(self, tags: str) -> str:
        return self.converter(tags).replace(" ", "\t_\t")

    def convert(self, sentence: List[dict], capitalize=True) -> str:
        first = sentence[0].copy()
        if capitalize:
            first['word'] = first['word'].capitalize()

        return reduce(plus,
                      (f"{i}\t{w['word']}\t{w['lemma']}\t{self._convert_to_ud(w['tag'])}\n" for i, w in
                       enumerate(cons(first, sentence[1:]), start=1)),
                      '').strip()
