from functools import lru_cache
from typing import Iterator, List

from cytoolz import identity

from _web_clients.http_session import HttpSession
from morph_service.word_token import WordItem
from tag_normalizer import TagNormalizer

__all__ = ['MorphClient']


class MorphClient:
    def __init__(self, uri='http://localhost', port=7419):
        self.session = HttpSession(f'{uri}:{port}')
        self.normalizer = TagNormalizer()

    @lru_cache(maxsize=4096)
    def parse_one(self, word: str, lexeme=False) -> List[WordItem]:
        response = self.session.get('morphy', word=word, lexeme=lexeme)
        response.encoding = 'UTF-8'
        return list(self._process_response(response.json(), False))

    def _normalize(self, tag: str) -> str:
        return self.normalizer.normalize(tag)

    def _process_response(self, words: List[dict], normalize: bool) -> Iterator[WordItem]:
        formatter = self.normalizer.normalize if normalize else identity
        for word in words:
            yield WordItem(word['word'], word['lemma'], formatter(word['tag']), word['score'], word.get('lexeme', None))

    def morph_sentence(self, sentence: str, normalize: bool = False) -> Iterator[WordItem]:
        response = self.session.get('omonimy', sentence=sentence)
        response.encoding = 'UTF-8'
        return self._process_response(response.json(), normalize)

    def get_prob(self, sentence: Iterator[WordItem]):
        response = self.session.post('prob', sentence=[{'tag': self.restore_tag(s.word, s.tag)} for s in sentence])
        response.encoding = 'UTF-8'
        res = response.json()
        return res

    def restore_tag(self, word, tag):
        n_tag = self.normalizer.normalize(tag)
        pm = next(pars for pars in self.parse_one(word) if self._normalize(pars.tag) == n_tag)
        return pm.tag

    def get_lemma(self, word: str, tag: str) -> str:
        n_tag = self.normalizer.normalize(tag)
        pm = next(pars for pars in self.parse_one(word) if self._normalize(pars.tag) == n_tag)
        return pm.lemma

    def get_wordform(self, word: str, tag: str, wanted_tag: str = None, wanted_word: str = None) -> WordItem:
        tag = self._normalize(tag)
        pm = next(pars for pars in self.parse_one(word, True) if self._normalize(pars.tag) == tag)
        if wanted_tag:
            wanted_tag = self._normalize(wanted_tag)
            wf = next(lx for lx in pm.lexeme if self._normalize(lx['tag']) == wanted_tag)
        else:
            wf = next(lx for lx in pm.lexeme if lx['word'] == wanted_word)

        return WordItem(wf['word'], wf['lemma'], self._normalize(wf['tag']), 1)


if __name__ == '__main__':
    from pprint import pprint

    mc = MorphClient()
    mmr = list(mc.morph_sentence('мама мыла раму.'))
    pprint(mmr)
    print('prob', mc.get_prob(mmr))
    pprint(list(x.as_dict() for x in mc.parse_one('мыла', True)))
    pprint(mc.get_wordform('мыла', mc.normalizer.normalize('NOUN,inan,neut sing,gent'),
                           mc.normalizer.normalize('NOUN,inan,neut plur,loct')))
