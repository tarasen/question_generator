import re
from functools import lru_cache

import matplotlib.pyplot as plt
import networkx
from networkx import draw_networkx, DiGraph, read_gpickle, write_gpickle, freeze

from _models.node import Node, MultiNode
from _web_clients.morph_client import MorphClient
from data_preparing.rules_source import rules, vocabulary, transforms
from morph_service.corpora_reader import CorporaReader
from morph_service.word_token import WordItem
from sentence_factory import SentenceFactory
from tag_normalizer import TagNormalizer

RE_STAR = re.compile('\*+')


def learn() -> DiGraph:
    from itertools import product

    from networkx import MultiDiGraph
    from tqdm import tqdm

    try:
        g = read_gpickle('../graph/corpora_rules2.gpickle')
    except:
        g = MultiDiGraph()
    tn = TagNormalizer()
    mc = MorphClient()
    sf = SentenceFactory(morph_client=mc, norm=tn)

    def get_addix(key, is_first=True):
        found = '^' if is_first else '$'
        suff, pref = [], []
        if '#' in key:
            arr = key.split('#')
            if len(arr) == 3:
                pref, key, suff = arr
                pref = [s.replace(found, '^') for s in pref.split('&') if found in s]
                suff = [s.replace(found, '^') for s in suff.split('&') if found in s]
            elif any(s in arr[0] for s in '^&$'):
                _pref, key = arr
                pref = [s.replace(found, '^') for s in _pref.split('&') if found in s]
            elif any(s in arr[1] for s in '^&$'):
                key, _suff = arr
                suff = [s.replace(found, '^') for s in _suff.split('&') if found in s]
        return pref, key, suff

    @lru_cache(maxsize=4096)
    def run_graph(key: str, value: str):
        if not key or not value:
            return

        for i in range(len(key.split('%'))):
            str_word_rule = RE_STAR.sub('', f'{key} {value}.'.replace('_', ' '))
            if '?' in str_word_rule:
                str_word_rule = str_word_rule.replace('?', '').replace('.', '?')

            keys = key.split(' ')
            values = value.split(' ')

            if '^' in str_word_rule:
                str_word_rule = str_word_rule.replace('^', '')
                key = next(it for it in keys if '^' not in it)
                value = next(it for it in values if '^' not in it)

            keys = [it.replace('^', '') for it in keys]
            values = [it.replace('^', '') for it in values]

            def get_word(token, tag):
                word = RE_STAR.sub('', token.replace('?', ''))
                lemma = mc.get_lemma(word, tag)
                return WordItem(word, lemma, tag, 1)

            try:
                morph_keys = [get_word(tok, tag) for k in (*keys, *values) for tok, tag in
                              zip(k.split('_'),
                                  [vocabulary[k].split('%')[i]] if '%' in vocabulary[k] else vocabulary[k].split('|'))]
                morph_keys += [
                    WordItem('.' if '?' not in str_word_rule else '?', '.' if '?' not in str_word_rule else '?', 'PNCT',
                             1)]
            except:
                print(keys, '|', values)
                morph_keys = None

            sent = sf.parse(str_word_rule, syntax=True, morph=morph_keys)[:-1]

            key_word, value_word = Node.select_word(key), Node.select_word(value)
            kk = key_word.take_from_sent(sent)
            vv = value_word.take_from_sent([s for s in sent if s not in key_word.parsed])
            if not kk or not vv:
                pass
            key_word.fix_with(value_word)

            if not key_word.is_question:
                k_node = key_word.node
            else:
                k_node = key_word.word + '?' + key_word.node
            if not k_node in g:
                if '|' in k_node:
                    a,b = key_word.parsed
                    child = a if a.link==b else b if b.link==a else None

                    g.add_node(k_node, deprel=child and child.deprel, word=key_word.word, direction=child==a)
                else:
                    g.add_node(k_node, word=key_word.word)
            if not value_word.node in g:
                if '|' in value_word.node:
                    a, b = value_word.parsed
                    child = a if a.link == b else b if b.link == a else None

                    g.add_node(value_word.node, deprel=child and child.deprel, word=value_word.word, direction=child == a)
                else:
                    g.add_node(value_word.node, word=value_word.word)
            # g.add_node(k_node)
            # g.add_node(value_word.node)

            path_type = key_word.deprel or value_word.deprel
            if path_type:
                g.add_edge(k_node, value_word.node, type='rule', direction=bool(key_word.deprel), syntax=path_type)
                # g.add_edge(k_node, value_word.node, path=kk + vv, type='rule', path_type=path_type)

    # @lru_cache()
    def parse_key_value(key_val: str, value_val: str) -> None:
        if not key_val or not value_val or '?' in value_val:
            return

        assert ('#' in key_val) == any(it in '^$' for it in key_val), key_val
        assert key_val.count('#') <= 2 and key_val.count('#') <= key_val.count('^') + key_val.count('$'), key_val
        assert ('#' in value_val) == any(it in '^$' for it in value_val), value_val
        assert value_val.count('#') <= 2 and value_val.count('#') <= value_val.count('^') + value_val.count(
            '$'), value_val

        pref_k, key_val, suff_k = get_addix(key_val)
        pref_v, value_val, suff_v = get_addix(value_val, is_first=False)
        assert key_val in vocabulary and value_val in vocabulary, key_val + ' ' + value_val

        for pk in pref_k:
            assert pk.replace('^', '') in vocabulary, pk
            run_graph(pk + ' ' + key_val, value_val)
        for sk in suff_k:
            assert sk.replace('^', '') in vocabulary, sk
            run_graph(key_val + ' ' + sk, value_val)
        for pv in pref_v:
            assert pv.replace('^', '') in vocabulary, pv
            run_graph(key_val, pv + ' ' + value_val)
        for sv in suff_v:
            assert sv.replace('^', '') in vocabulary, sv
            run_graph(key_val, value_val + ' ' + sv)
        run_graph(key_val, value_val)

    rul = [(k, r) for k, v in rules.items() for r in v]
    for pair in tqdm(rul, total=len(rul)):
        parse_key_value(*pair)

    for kk, v in transforms.items():
        for tk in vocabulary[kk].split('%'):
            key = (RE_STAR.sub('', kk) + tn.normalize(tk)) if '?' in kk else tn.normalize(tk)
            vals = []
            for ww in v:
                for tw in vocabulary[ww].split('%'):
                    vals.append((RE_STAR.sub('', ww) + tn.normalize(tw)) if '?' in ww else tn.normalize(tw))
            pairs = product([key], vals)
            g.add_edges_from(pairs, type='transform')

    return g


def read_or_load(path: str, force_learn: bool = False) -> DiGraph:
    from pathlib import Path
    if not force_learn and Path(path).is_file():
        print('read pickle')
        g = read_gpickle(path)
    else:
        print('learning')
        g = learn()
        freeze(g)
        write_gpickle(g, path)
    return g


if __name__ == '__main__':
    g = read_or_load('../graph/rules_graph.gpickle')

    draw_networkx(g)
    plt.show()
