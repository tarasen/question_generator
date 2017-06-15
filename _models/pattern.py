from typing import List, Iterable

from cytoolz import memoize

from _models.rule_item import RuleItem
from settings import Settings


class Pattern:
    tagset = None

    def __init__(self, rules: List[RuleItem], sent_tags: Iterable[str], quest_tags: Iterable[str],
                 answer: List[RuleItem]):
        self.__rules = rules
        self.__quest_tags = list(quest_tags)
        self.__sent_tags = list(sent_tags)
        self.__answer = answer

        self.__has_copy = any(pt.tag == Settings.COPY_KEY for pt in rules)
        self.__has_transform = any(pt.tag == Settings.RULE_KEY for pt in rules)

    @classmethod
    def set_tagset(cls, tagset):
        cls.tagset = tagset

    @staticmethod
    @memoize()
    def get_grammemes(tag):
        return Settings.TAG_CLASS(tag).grammemes

    @staticmethod
    @memoize()
    def calc_tags(tag1, tag2):
        rule_sent = Pattern.get_grammemes(tag1)
        rule_quest = Pattern.get_grammemes(tag2)

        disappeared_rule = frozenset(rule_sent - rule_quest)
        disappeared_rule_group = frozenset(k for k, v in Pattern.tagset.items() if disappeared_rule & v)

        appeared_rule = frozenset(rule_quest - rule_sent)
        appeared_rule_group = frozenset(k for k, v in Pattern.tagset.items() if appeared_rule & v)

        return disappeared_rule, disappeared_rule_group, appeared_rule, appeared_rule_group, rule_quest

    @property
    def has_copy(self):
        return self.__has_copy

    @property
    def has_tag_transform(self):
        return self.__has_transform

    def as_dict(self):
        return {'rules': list(map(lambda r: r.as_dict(), self)),
                'answer': list(map(lambda r: r.as_dict(), self.__answer)),
                'sent_tags': self.__sent_tags, 'quest_tags': self.__quest_tags, }

    @staticmethod
    def from_dict(dct):
        return Pattern([RuleItem(r['tag'], r['link'], r['rule'], r['morph']) for r in dct['rules']], dct['sent_tags'],
                       dct['quest_tags'],
                       [RuleItem(r['tag'], r['link'], r['rule'], r['morph']) for r in dct['answer']])

    @property
    def quest_tags(self):
        return self.__quest_tags

    @property
    def sent_tags(self):
        return self.__sent_tags

    @property
    def answer(self):
        return self.__answer

    def __eq__(self, other):
        return isinstance(other, Pattern) and len(self) == len(other) and all(r == o for r, o in zip(self, other))

    def __getitem__(self, item):
        return self.__rules[item]

    def __len__(self):
        return len(self.__rules)

    def __iter__(self):
        return iter(self.__rules)

    def __repr__(self):
        return '|'.join(map(repr, self.__rules))
