from cytoolz import count, first

from syntax_service.conllu_converter import CONLLUConverter
from syntax_service.maltparser import MaltRunner


class SyntaxAnalyzer:
    def __init__(self):
        self.conllu = CONLLUConverter()
        self.maltparser = MaltRunner()

    def build_syntax(self, sentence):
        conllu = self.conllu.convert(sentence)
        deps = first(self.maltparser.parse_many([conllu])).strip().split('\n')

        if count(t for t in deps if 'ROOT' in t) > 1:
            conllu = self.conllu.convert(sentence, False)
            deps2 = first(self.maltparser.parse_many([conllu])).strip().split('\n')
            deps = deps if count(t for t in deps2[1] if t == 'ROOT') > 1 else deps2

        for l2 in deps:
            a, b = l2.split('\t')[:2]
            a = int(a) - 1
            yield (a, b)
        yield (-1, '_')
