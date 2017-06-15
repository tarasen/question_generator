from collections import defaultdict
from copy import deepcopy, copy
from itertools import product, combinations, filterfalse
from multiprocessing.dummy import Pool as ThreadPool
from operator import itemgetter, attrgetter
from random import shuffle
from typing import Set, FrozenSet, Tuple, Iterable, List

from cytoolz import valfilter, excepts, first, concat, get, get_in, unique, pluck, mapcat, partition_all

from _models.node import Node
from _models.pattern import Pattern
from _models.sentence import Sentence
from _models.substitution import Substitution
from _models.substitutions import Substitutions
from _models.syntax_item import SyntaxItem
from _models.transform import Transform
from filter import Filter
from lib_ex.ftools import pluck_attr, c_in
from morph_service.word_token import WordItem
from settings import Settings
from tree_cutter import TreeCutter


def index_of(seq: iter, val: object, default: object = -1) -> int:
    return excepts(ValueError, lambda a: seq.index(a), lambda _: default)(val)


def remove_subsets(items: Iterable) -> Set:
    sets = set(items)
    us = set()
    while sets:
        e = sets.pop()
        if not any(e.issubset(s) for s in sets) and not any(e.issubset(s) for s in us):
            us.add(e)
    return us


Pattern.set_tagset(Settings.tagset_dict)


class Transformer:
    def __init__(self, sentence, graph, mc):
        self.sentence = sentence
        self.graph = graph
        self.mc = mc

        self.num_parts = 2
        self.pool = ThreadPool(self.num_parts)

        self.filter = Filter(mc)
        self.transforms = self.find_transforms(sentence, self.graph)
        self.sent_groups = self._group_sent(self.transforms)
        self.subs = [(c, self.__get_substitutions(c)) for c in self.sent_groups]
        shuffle(self.subs)

        #  @timeout(120)

    def process_question(self, question: Sentence, pattern: Pattern) -> List[Tuple[Sentence, Sentence]]:
        transforms = self.find_transforms(question, self.graph)
        # for trans in transforms.copy():
        #     if all(pattern[i].tag == Settings.QUESTION_WORD_KEY for i in trans.numbers):
        #         transforms.remove(trans)

        q_sub = [(c, self.__get_substitutions(c)) for c in self._group_sent(transforms)]

        prod_count = len(self.subs) * len(q_sub)

        if True:  # prod_count < 100000:
            # t = time()
            filtered = [(s, q) for s, q in product(self.subs, q_sub) if
                        self._filter_combination(s[1], q[1], pattern)]
        # print('seq', time() - t, '; count', len(filtered))
        else:
            # t = time()
            shuffle(q_sub)

            filt_fir = lambda fir: [(s, q) for s, q in product(fir, q_sub) if
                                    self._filter_combination(s[1], q[1], pattern)]
            filt_sec = lambda sec: [(s, q) for s, q in product(self.subs, sec) if
                                    self._filter_combination(s[1], q[1], pattern)]

            if len(self.subs) > len(q_sub):
                chunk = (len(self.subs) // self.num_parts) + 1
                results = self.pool.map(filt_fir, partition_all(chunk, self.subs))
            else:
                chunk = (len(q_sub) // self.num_parts) + 1
                results = self.pool.map(filt_sec, partition_all(chunk, q_sub))

            filtered = list(concat(results))
            # print('par', time() - t, '; count', len(filtered))

        sent_combs = {sub: self._apply_to_sentence(self.sentence, c) for c, sub in
                      unique(pluck(0, filtered), key=itemgetter(1))}
        quest_combs = {sub: self._apply_to_sentence(question, c) for c, sub in
                       unique(pluck(1, filtered), key=itemgetter(1))}

        trues = [(sent_combs[s[1]], quest_combs[q[1]]) for s, q in filtered]

        # result = sorted(tuple(pluck_attr('original', t)) for t in trues)
        # sz = len(result)

        return [(s, q) for s, q in trues if s.original != self.sentence.original or q.original != question.original]

    def _get_groups(self, transforms: List[Transform]) -> Set[
        FrozenSet[Tuple[FrozenSet[int], Tuple[str, str], Tuple[str, str]]]]:
        if len(transforms) == 1:
            return {frozenset(((frozenset(), first(transforms).key, first(transforms).key),))}

        gr = defaultdict(set)
        not_gr = set()
        for s1, s2 in combinations(transforms, 2):
            intersect = s1.numbers & s2.numbers
            if intersect:
                to_add = (frozenset(intersect), s1.key, s2.key)
                for it in gr.values():
                    if any(x in (s1.key, s2.key) for x in concat(get([1, 2], a) for a in it)):
                        it.add(to_add)
                gr[s1.key].add(to_add)
                gr[s2.key].add(to_add)
            else:
                not_gr |= {s1.key, s2.key}
        for key in filterfalse(c_in(gr), not_gr):
            gr[key].add((frozenset(), key, key))
        return remove_subsets(map(frozenset, gr.values()))

    def _get_results(self, transforms: List[Transform], groups):
        res = []
        selector = lambda x: next(t for t in transforms if t.key == x)
        for group in ([(its, selector(a), selector(b)) for its, a, b in group] for group in groups):
            for its, v1, v2 in group:
                v1_i, v2_i = int(its <= v1.node_b.numbers), int(its <= v2.node_b.numbers)
                grp = [(v1, v2, t1, t2, v1_i, v2_i) for t1, t2 in product(v1.variants, v2.variants) if
                       t1[v1_i] == t2[v2_i]]
                if not res:
                    res = [[l] for l in grp]
                elif grp:
                    prv = list(filter(lambda p: p[1] != 1,
                                      ((i, 2 + index_of(a[0:2], v1)) for i, a in enumerate(res[0]))))
                    nxt = list(filter(lambda p: p[1] != 1,
                                      ((i, 2 + index_of(a[0:2], v2)) for i, a in enumerate(res[0]))))

                    if not prv and not nxt:
                        res = [line + [l] for line, l in product(res, grp)]
                    elif prv and not nxt:
                        res = [line + [l] for line, l in product(res, grp) if all(l[2] == get_in(p, line) for p in prv)]
                    elif not prv and nxt:
                        res = [line + [l] for line, l in product(res, grp) if all(l[3] == get_in(n, line) for n in nxt)]
                    else:
                        res = [line + [l] for line, l in product(res, grp) if
                               all(l[2] == get_in(p, line) and l[3] == get_in(n, line) for n in nxt for p in prv)]
        return res

    @staticmethod
    def find_transforms(sentence, graph):
        def are_in_graph(n1: str, n2: str, direct: bool):
            return n1 in graph and n2 in graph and \
                   (n2 in graph[n1] and any(
                       t['type'] == 'rule' and t['direction'] == direct for t in graph[n1][n2].values())
                    or n1 in graph[n2] and any(
                       t['type'] == 'rule' and t['direction'] == (not direct) for t in graph[n2][n1].values()))

        def is_path_type_equal(n1: str, n2: str, link: str, direct: bool):
            return n2 in graph[n1] and any(
                t['syntax'] == link and t['direction'] == direct for t in graph[n1][n2].values()) or \
                   n1 in graph[n2] and any(
                       t['syntax'] == link and t['direction'] == (not direct) for t in graph[n2][n1].values())

        def all_neighbors(nodes):
            f = 0
            nd = set(nodes)
            while f != len(nd):
                f = len(nd)
                nd |= {ngb for n in nd for ngb in graph.neighbors(n) if
                       any(t['type'] == 'transform' for t in graph[n][ngb].values())}
            return nd

        _transforms = {}
        for a, b in ((w, w.link) for w in sentence[:-1] if
                     w.link is not None and not w.is_root and w.tag != 'PNCT' and w.link.pos != 'PNCT'):
            words = (a.word, b.word)
            a_rel, b_rel = map(Node.select_word,
                               map(lambda w: w + '?' if w in Settings.russian_question_words else w, words))
            a_rel.take_from_sent([a])
            b_rel.take_from_sent([b])
            if not a_rel.fix_with(b_rel):
                continue
            k_node, v_node = a_rel.node, b_rel.node
            if not are_in_graph(k_node, v_node, a.number < b.number) or not is_path_type_equal(k_node, v_node, a.deprel,
                                                                                               a.number < b.number):
                if a_rel.is_question:
                    k_node = a_rel.word + '?' + a_rel.node
                if (k_node == a_rel.node) or \
                        not are_in_graph(k_node, v_node, a.number < b.number) or \
                        not is_path_type_equal(k_node, v_node, a.deprel, a.number < b.number):
                    continue

            n1_neig = all_neighbors([k_node])
            n2_neig = all_neighbors([v_node])
            new_path = {(t1, t2) for (t1, t2) in product(n1_neig, n2_neig) if
                        (t2 in graph[t1] and any(
                            t['type'] == 'rule' and t['direction'] == a.number < b.number and t['syntax'] == a.deprel
                            for t in graph[t1][t2].values()) or
                         (t1 in graph[t2] and any(
                             t['type'] == 'rule' and t['direction'] == a.number > b.number and t['syntax'] == a.deprel
                             for t in graph[t2][t1].values())))}

            _transforms[words] = Transform(a_rel, b_rel, new_path)

        for s, links in TreeCutter(sentence, check_root=False):
            fs = s[:-1]
            if len(fs) > 4:
                break
            words = [w.word for w in fs]

            ex_found = False
            for w in filter(lambda w: w.word in Settings.prefixes, fs):
                if w.head > -1:
                    nx = fs[w.head]
                    words[nx.number] = f'{w.word}_{nx.word}'
                    words.remove(words[w.number])
                    ex_found = True
            if not ex_found:
                continue

            relations = list(
                map(Node.select_word, map(lambda w: w + '?' if w in Settings.russian_question_words else w, words)))
            for i, rel in enumerate(relations):
                rel.take_from_sent([s for s in sentence if s not in mapcat(attrgetter('parsed'), relations[:i])])

            for key, value in filter(lambda p: p[0].is_links_to(p[1]), combinations(relations, 2)):
                key, value = deepcopy(key), deepcopy(value)
                key.fix_with(value)

                if (key.word, value.word) in _transforms:
                    continue

                k_node, v_node = key.node, value.node
                if not are_in_graph(k_node, v_node) or not is_path_type_equal(k_node, v_node,
                                                                              (key.deprel, value.deprel)):
                    if key.is_question:
                        k_node = key.word + '?' + key.node
                    if (k_node == key.node) or \
                            not are_in_graph(k_node, v_node) or \
                            not is_path_type_equal(k_node, v_node, (key.deprel, value.deprel)):
                        continue

                n1_neig = all_neighbors([k_node])
                n2_neig = all_neighbors([v_node])
                new_path = {(a, b) for (a, b) in product(n1_neig, n2_neig) if
                            b in graph[a] and any(t['type'] == 'rule' for t in graph[a][b].values())}

                _transforms[(key.word, value.word)] = Transform(key, value, new_path)

        us = remove_subsets(e.numbers for e in _transforms.values())
        return list(valfilter(lambda t: t.numbers in us, _transforms).values())

    def _group_sent(self, transforms):
        return self._get_results(transforms, self._get_groups(transforms))

    @staticmethod
    def __get_substitutions(sent_change) -> FrozenSet[Substitution]:
        res = []
        for sc in sent_change:
            for i in range(2):
                res.append(Substitution(sc[i].node_a.numbers, sc[i].node_a.lemmas, sc[2 + i][0]))
                res.append(Substitution(sc[i].node_b.numbers, sc[i].node_b.lemmas, sc[2 + i][1]))
        return Substitutions(res)

    def _filter_combination(self, s_sub: Substitutions, q_sub: Substitutions, pattern: Pattern):
        passed = True

        if pattern.has_tag_transform:
            passed = passed and self.filter.rule_tag_filter(s_sub, q_sub, pattern)
        else:
            passed = passed and self.filter.tagset_filter(s_sub, q_sub)

        if pattern.has_copy:
            passed = passed and self.filter.fixed_point_filter(s_sub, q_sub, pattern)

        # if any(pt.tag == Settings.QUESTION_KEY for pt in pattern):
        #     passed = passed and self.filter.question_filter(q_comb, pattern, question)

        return passed

    def _apply_to_word(self, source: List[SyntaxItem], dest: List[SyntaxItem], sentence: Sentence):
        add, rem = None, None
        if len(dest) == len(source):
            for f, t in ((f, t) for f, t in zip(source, dest) if f.tag != t.tag):
                try:
                    t.base = self.mc.get_wordform(f.word, f.tag, t.tag)
                except StopIteration:
                    pass
                sentence[f.number].base = t
        elif len(dest) > len(source):
            main = next((a for a in dest if a.is_root), None) or next(filter(lambda a: a.link not in dest, dest))
            try:
                main.base = self.mc.get_wordform(source[0].word, source[0].tag, main.tag)
            except StopIteration:
                pass
            sentence[source[0].number].base = main

            add = (sentence[source[0].number], dest)
        else:
            while len(dest) > 0:
                main_s = next((a for a in source if a.is_root), None) or next(
                    filter(lambda a: a.link not in source, source))
                source.remove(main_s)
                main_d = next((a for a in dest if a.is_root), None) or next(filter(lambda a: a.link not in dest, dest))
                dest.remove(main_d)

                try:
                    main_d.base = self.mc.get_wordform(main_s.word, main_s.tag, main_d.tag)
                except StopIteration:
                    pass
                sentence[main_s.number].base = main_d

            for f in source:
                del sentence[f.number].base
            rem = source

        return add, rem

    def _apply_to_sentence(self, sent: Sentence, changes) -> Sentence:
        new_sent = deepcopy(sent)
        looks, edits = [], []
        l_copy = lambda c: list(map(deepcopy, c))

        for pair in changes:
            p = pair[:4]
            for a, b, rule in ((p[0 + i].parsed_a, p[0 + i].parsed_b, p[2 + i]) for i in range(2) if
                               p[2 + i] not in looks):
                looks.append(rule)

                if any('|' in r for r in rule):
                    w1, w2 = self.graph.node[rule[0]], self.graph.node[rule[1]]
                    if 'deprel' in w1:
                        fr = [SyntaxItem(i, w, None, t, 1, -1, w1['deprel']) for i, (w, t) in
                              enumerate(zip(w1['word'].split('_'), rule[0].split('|')))]
                        if w1['direction']:
                            fr[0].head, fr[1].deprel = 1, 'root'
                            fr[0].set_link(fr[1])
                        else:
                            fr[1].head, fr[0].deprel = 0, 'root'
                            fr[1].set_link(fr[0])
                    else:
                        fr = [WordItem(w1['word'], None, rule[0], 1)]
                    if 'deprel' in w2:
                        to = [SyntaxItem(i, w, None, t, 1, -1, w2['deprel']) for i, (w, t) in
                              enumerate(zip(w2['word'].split('_'), rule[1].split('|')))]
                        if w2['direction']:
                            to[0].head, to[1].deprel = 1, 'root'
                            to[0].set_link(to[1])
                        else:
                            to[1].head, to[0].deprel = 0, 'root'
                            to[1].set_link(to[0])
                    else:
                        to = [WordItem(w1['word'], None, rule[1], 1)]
                else:
                    fr, to = [WordItem(self.graph.node[rule[0]]['word'], None, rule[0], 1)], [
                        WordItem(self.graph.node[rule[1]]['word'], None, rule[1], 1)]

                if tuple(pluck_attr('tag', a)) != tuple(pluck_attr('tag', fr)):
                    edits.append(self._apply_to_word(l_copy(a), fr, new_sent))

                if tuple(pluck_attr('tag', b)) != tuple(pluck_attr('tag', to)):
                    edits.append(self._apply_to_word(l_copy(b), to, new_sent))

        added = list(unique(filter(bool, pluck(0, edits)), key=lambda a: a[0].number))
        removed = list(unique(filter(bool, pluck(1, edits)), key=lambda a: a[0].number))

        if not added and not removed:
            return new_sent

        # renumerate
        if added:
            for a, rul in sorted(added, key=lambda a: a[0].number, reverse=True):
                d = {i: i + len(rul) - 1 for i in range(a.number + 1, len(new_sent))}
                d[a.number] = a.number + next((i for i in range(len(rul)) if rul[i].base == a.base), 0)
                for w in (w for w in new_sent if w.number != a.number):
                    if w.number in d:
                        w.number = d[w.number]
                    if w.head in d:
                        w.head = d[w.head]
                for i, r in enumerate(rul):
                    r.number = a.number + i
                    r.head = -1 if r.head == -1 else a.number + r.head - 1
                new_sent.insert(a.number, a.number + 1, rul)
            new_sent.init_links()

        if removed:
            d = {v: i for i, v in enumerate(it.number for it in new_sent if it.base != ('', '', ''))}
            d[-1] = -1
            for w in copy(new_sent):
                if w.base == ('', '', ''):
                    del new_sent[w]
                else:
                    w.number = d[w.number]
                    if w.head in d:
                        w.head = d[w.head]
                    else:
                        x = w.head
                        while x not in d:
                            x = next(ns.head for ns in new_sent if ns.number == x)
                        w.head = d[x]

        if 'ROOT' in (w.deprel for w in new_sent):
            for w in (w for w in new_sent if 'root' == w.deprel):
                w.deprel = 'ROOT'

        return new_sent
