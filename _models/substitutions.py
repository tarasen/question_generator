from typing import Iterator

from _models.pattern import Pattern
from _models.substitution import Substitution
from lib_ex.ftools import pluck_attr


class Substitutions:
    def __init__(self, subs: Iterator[Substitution]):
        self.subs = frozenset(subs)
        self.tags = None

    def __iter__(self):
        return iter(self.subs)

    def extract_tags(self):
        if not self.tags:
            self.tags = frozenset(pluck_attr('tag', (gr for gr in self.subs if not gr.is_question)))
        return self.tags