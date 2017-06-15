from typing import Tuple


class RuleItem:
    def __init__(self, tag: str, link: int, rule: Tuple[str, str] = None, morph: str = None):
        self.__tag = tag
        self.__link = link
        self.__rule = rule and tuple(rule)
        self.__morph = morph

    @property
    def tag(self) -> str:
        return self.__tag

    @property
    def link(self) -> int or str:
        return self.__link

    @property
    def rule(self) -> Tuple[str, str]:
        return self.__rule

    @property
    def morph(self) -> str:
        return self.__morph

    def as_dict(self):
        return {'rule': self.rule, 'link': self.link, 'tag': self.tag, 'morph': self.__morph}

    def __str__(self):
        return f'tag:{self.tag[0]}, rule:{self.rule}, link:{self.link}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'RuleItem'):
        return self.tag == other.tag and self.link == other.link and self.rule == other.rule and self.__morph == other.__morph
