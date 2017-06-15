from copy import deepcopy
from itertools import permutations
from operator import itemgetter
from sys import intern
from typing import List

import networkx
from cytoolz import groupby, cons
from networkx.readwrite import json_graph

from _models.sentence import Sentence, DummySentence
from _web_clients.morph_client import MorphClient
from _web_clients.syntax_client import SyntaxClient
from morph_service.word_token import WordItem
from tag_normalizer import TagNormalizer


class SentenceFactory:
    def __init__(self, morph_client: MorphClient = None, norm: TagNormalizer = None):
        self.mc = morph_client or MorphClient()
        self.norm = norm or TagNormalizer()
        self.sc = SyntaxClient()

    def parse(self, sentence: str, syntax=True, morph: List[WordItem] = None) -> Sentence:
        words = morph or list(self.mc.morph_sentence(sentence))
        if syntax:
            words = list(self.sc.parse(words))
        for word in words:
            word.tag = self.norm.normalize(word.tag)

        return Sentence(words) if syntax else DummySentence(words)

    def resyntax(self, sentence: 'Sentence'):
        words = deepcopy(sentence)
        for word in words:
            word.tag = self.mc.restore_tag(word.word, word.tag)
        for orig, word in zip(sentence, self.sc.parse(words)):
            orig.fix_syntax(word)
        sentence.init_links()

    def get_json(self, sentence):
        key = [[i, self.norm.normalize(k[0]), k[1], intern(k[2])] for i, k in enumerate(sentence[:-1])]

        key = sorted([(k[0], k[1] + '_' + str(i), k[2], k[3]) for x in groupby(itemgetter(1), key).values() for i, k in
                      enumerate(sorted(x, key=itemgetter(0)))], key=itemgetter(0))
        nx = networkx.DiGraph()
        nx.add_node('root')
        key = list(map(tuple, key))
        edges = {((a[:2], a[3], b[:2]) if a[2] == b[0] else (b[:2], b[3], a[:2])) for a, b in
                 permutations(cons((-1, 'root', -1, None), key), 2) if a[0] == b[2] or a[2] == b[0]}
        for e in edges:
            nx.add_edge(e[2][1], e[0][1], type=e[1])

        data = json_graph.node_link_data(nx)
        return data, nx
