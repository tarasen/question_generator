from typing import List

from cytoolz import valfilter
from pymorphy2 import MorphAnalyzer
from pymorphy2.tagset import OpencorporaTag

__all__ = ['Settings']


def read_zipfile(path: str) -> List[str]:
    with open(path, 'rt') as f:
        return f.read().split('\n')


tc = MorphAnalyzer().TagClass
tagset_d = valfilter(lambda v: type(v) is frozenset,
                     {key: getattr(tc('NOUN'), key) for key in dir(OpencorporaTag) if
                      not key.startswith('_') and key.isupper()})


class Settings:
    russian_question_words = frozenset(read_zipfile("c:/temp/12/russian_question_words.txt"))
    russian_hard_questions = frozenset(read_zipfile("c:/temp/12/russian_hard_questions.txt"))

    prefixes = frozenset(['будет', 'будут', 'буду', 'будем', 'будешь', 'будете'])
    suffixes = frozenset()

    PUNCT_KEY = 'punct'
    COPY_KEY = 'copy'
    NEW_TOKEN_KEY = 'leave'
    RULE_KEY = 'rule'
    QUESTION_KEY = 'question'
    QUESTION_WORD_KEY = 'question'
    ANSWER_KEY = 'answer'

    TAG_CLASS = tc
    tagset_dict = tagset_d

    deps = {
        'Nominals': ['nsubj', 'nsubj:pass', 'obj', 'iobj',
                     'obl', 'obl:agent', 'vocative', 'expl', 'dislocated',
                     'nmod', 'appos', 'nummod', 'nummod:gov'],
        'Clauses': ['csubj', 'csubj:pass', 'ccomp', 'xcomp', 'advcl', 'acl', 'acl:relcl'],
        'ModifierWords': ['advmod', 'discourse', 'amod'],
        'FunctionWords': ['aux', 'aux:pass', 'cop', 'mark', 'det', 'case'],

        'Coordination': ['conj', 'cc'],
        'MWE': ['fixed', 'flat', 'compound'],
        'Loose': ['list', 'parataxis'],
        'Special': ['orphan', 'goeswith', 'reparandum'],
        'Other': ['punct', 'root', 'dep', 'ROOT'],

        'CoreArguments': ['nsubj', 'nsubj:pass', 'obj', 'iobj',
                          'csubj', 'csubj:pass', 'ccomp', 'xcomp'],
        'NonCoreDependents': ['obl', 'obl:agent', 'vocative', 'expl', 'dislocated', 'advcl', 'advmod', 'discourse',
                              'aux',
                              'aux:pass', 'cop', 'mark'],
        'NominalDependents': ['nmod', 'appos', 'nummod', 'nummod:gov', 'acl', 'acl:relcl', 'amod', 'det', 'case']
    }
