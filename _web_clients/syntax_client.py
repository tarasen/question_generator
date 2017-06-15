from typing import Iterator

from _models.syntax_item import SyntaxItem
from _web_clients.http_session import HttpSession
from morph_service.word_token import WordItem

__all__ = ['SyntaxClient']


class SyntaxClient:
    def __init__(self, uri='http://localhost', port=7418):
        self.session = HttpSession(f'{uri}:{port}')

    def parse(self, sentence: Iterator[WordItem]) -> Iterator[SyntaxItem]:
        response = self.session.post('parse', sentences=[s.as_dict() for s in sentence])
        response.encoding = 'UTF-8'
        return (SyntaxItem(i, d['word'], d['lemma'], d['tag'], d['score'], d['head'], d['deprel']) for i, d in
                enumerate(response.json()))


if __name__ == '__main__':
    from pprint import pprint
    from _web_clients.morph_client import MorphClient

    mc = MorphClient()
    sc = SyntaxClient()
    snt = list(mc.morph_sentence('мама мыла раму.'))
    p = list(sc.parse(snt))
    pprint(p)
