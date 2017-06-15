from typing import Set

from cytoolz import first, last

from _models.pattern import Pattern
from _models.sentence import Sentence
from _models.substitution import Substitution
from _models.substitutions import Substitutions
from _web_clients.morph_client import MorphClient
from lib_ex.ftools import pluck_attr
from settings import Settings


class Filter:
    def __init__(self, mc: MorphClient):
        self.mc = mc
        self.settings = Settings

    def fixed_point_filter(self, a: Substitutions, b: Substitutions, pattern: Pattern) -> bool:
        for it in b:
            if len(it.numbers) == 1:
                pt = pattern[first(it.numbers)]
                if pt.tag == self.settings.COPY_KEY:
                    lnk = next((fr for fr in a if pt.link in fr.numbers), None)
                    if lnk is None or lnk.tag != it.tag or lnk.lemmas != it.lemmas:
                        return False
            else:
                pt = next((pattern[k] for k in it.numbers if pattern[k].tag == self.settings.COPY_KEY), None)
                if pt:
                    lnk = next((fr for fr in a if pt.link in fr.numbers), None)
                    if lnk is None or lnk.tag != it.tag or not lnk.lemmas & it.lemmas:
                        return False
        return True

    def tagset_filter(self, a: Substitutions, b: Substitutions) -> bool:
        return a.extract_tags() >= b.extract_tags()

    def rule_tag_filter(self, a: Substitutions, b: Substitutions, pattern: Pattern) -> bool:
        for it in b:
            if len(it.numbers) == 1:
                pt = pattern[first(it.numbers)]
                if pt.tag == self.settings.RULE_KEY:
                    lnk = next((fr for fr in a if pt.link in fr.numbers), None)
                    if lnk is None or len(lnk.tags) != len(it.tags):
                        return False

                    disappeared_rule, disappeared_rule_group, appeared_rule, appeared_rule_group, _ = Pattern.calc_tags(
                        pt.rule[0], pt.rule[1])

                    for sp, qp in zip(lnk.tags, it.tags):
                        disap_ptrn, disap_ptrn_grp, app_ptrn, app_ptrn_grp, q_gr = Pattern.calc_tags(sp, qp)

                        if not (disap_ptrn_grp <= disappeared_rule_group) or not (app_ptrn_grp <= appeared_rule_group):
                            return False
                        if (disap_ptrn_grp == disappeared_rule_group and app_ptrn_grp == appeared_rule_group) \
                                and appeared_rule != app_ptrn:
                            return False
                        if (disap_ptrn_grp <= disappeared_rule_group and app_ptrn_grp <= appeared_rule_group) \
                                and appeared_rule != app_ptrn and disappeared_rule != disap_ptrn:
                            tot = q_gr & {val for k in appeared_rule_group for val in self.settings.tagset_dict[k]}
                            if tot and appeared_rule != tot:
                                return False

        return True

    def length_filter(self, a: Substitutions, b: Substitutions, pattern: Pattern) -> bool:
        for it in b:
            if len(it.numbers) == 1:
                pt = pattern[first(it.numbers)]
                if pt.tag == self.settings.RULE_KEY:
                    lnk = next((fr for fr in a if pt.link in fr.numbers), None)
                    if lnk is None or len(lnk.tags) != len(it.tags):
                        return False
        return True

    def self_filter(self, a: Set[Substitution], b: Set[Substitution], sent: Sentence, quest: Sentence) -> bool:
        # return True
        r_a = {Substitution(frozenset([w.number]), frozenset([w.lemma]), w.tag) for w in sent[:-1]}
        r_b = {Substitution(frozenset([w.number]), frozenset([w.lemma]), w.tag) for w in quest[:-1]}

        q = next(('?' in t for t in pluck_attr('tag', b)), None) or set()
        if q:
            q_b = b - q
            q_b |= {Substitution(q.numbers, q.lemmas, last(q.tag.split('?')))}
        else:
            q_b = b
        return not (a <= r_a and q_b <= r_b)

    def question_filter(self, b: Substitutions, pattern: Pattern, quest: Sentence):
        for it in b:
            if len(it.numbers) == 1:
                pt = pattern[first(it.numbers)]
                if pt.tag == self.settings.QUESTION_KEY:
                    try:
                        self.mc.get_wordform(pt.link, quest[first(it.numbers)].tag, it.tag)
                    except StopIteration:
                        return False
        return True
