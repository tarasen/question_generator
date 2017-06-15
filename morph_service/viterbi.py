from itertools import starmap, product
from operator import itemgetter
from pprint import pprint
from typing import List, Dict, Tuple

from cytoolz import curried, frequencies, mapcat, get, first, drop, last, \
    groupby, compose

from morph_service.corpora_reader import CorporaReader
from morph_service.frequencyalg import FrequencyAlg
from morph_service.word_token import WordItem

__all__ = ['Viterbi']


class Viterbi(FrequencyAlg):
    START_SYMBOL = '<S>'
    END_SYMBOL = '</S>'
    LOW_PROB = 1e-10

    @staticmethod
    def __get_training_info(training_set: List[List[Tuple[str, str]]]) -> Dict[Tuple[str, str], float]:
        tag_counts = frequencies(mapcat(curried.pluck(1), training_set))
        tag_freq = frequencies(mapcat(compose(curried.sliding_window(2), curried.pluck(1)), training_set))
        delta = 0.0584560355383
        v = {k: delta * len(it) for k, it in groupby(itemgetter(1), tag_freq.keys()).items()}
        return {(a, b): (get((a, b), tag_freq, 0) + delta) / (get(b, tag_counts, 0) + get(b, v, delta)) for a, b in
                product(tag_counts.keys(), repeat=2)}

    def __init__(self, corpora_path: str):
        super().__init__()
        tagged_sents = CorporaReader.read_opencorpora(corpora_path, self.START_SYMBOL, self.END_SYMBOL)

        self.cpd_tags = self.__get_training_info(tagged_sents)

    def prob(self, prev: str, nxt: str) -> float:
        return self.cpd_tags.get((prev, nxt), self.LOW_PROB)

    def parse_sentence(self, sentence: List[str]) -> List[WordItem]:
        viterbi = []
        backpointer = []

        first_viterbi = {}
        first_backpointer = {}
        for parsed in self.morphy(first(sentence)):
            tag = parsed.tag
            first_viterbi[tag] = self.prob(self.START_SYMBOL, tag) * parsed.score
            first_backpointer[tag] = self.START_SYMBOL

        viterbi.append(first_viterbi)
        backpointer.append(first_backpointer)

        for word in drop(1, sentence):
            this_viterbi = {}
            this_backpointer = {}
            prev_viterbi = last(viterbi)

            for parsed in self.morphy(word):
                tag = parsed.tag
                best_previous = max(prev_viterbi,
                                    key=lambda prevtag: prev_viterbi[prevtag] * self.prob(prevtag, tag) * parsed.score)

                this_viterbi[tag] = prev_viterbi[best_previous] * self.prob(best_previous, tag) * parsed.score
                this_backpointer[tag] = best_previous

            viterbi.append(this_viterbi)
            backpointer.append(this_backpointer)

        prev_viterbi = last(viterbi)
        best_previous = max(prev_viterbi,
                            key=lambda prevtag: prev_viterbi[prevtag] * self.prob(prevtag, self.END_SYMBOL))

        best_tagsequence = [self.END_SYMBOL, best_previous]

        current_best_tag = best_previous
        for bp in reversed(backpointer):
            best_tagsequence.append(bp[current_best_tag])
            current_best_tag = bp[current_best_tag]

        best_tagsequence.reverse()
        return list(starmap(self.select_word, zip(sentence, best_tagsequence[1:-1])))

    def select_word(self, token: str, tag: str) -> WordItem:
        return next(t for t in super().morphy(token) if t.tag == tag)


if __name__ == '__main__':
    v = Viterbi("c:/temp/ready2/corpus_train.txt")
    pprint(v.parse_sentence(['моя', 'мама', 'мыла', 'раму', 'долго', 'и', 'тщательно', '.']))
    # size = 100000
    # now = time.time()
    # for i in range(0, size):
    #     v.viterbi_alg(['моя', 'мама', 'мыла', 'раму', 'долго', 'и', 'тщательно', '.'])

    # print(v.viterbi_alg(['моя', 'мама', 'мыла', 'раму', 'долго', 'и', 'тщательно', '.']))
    # print("Finished in", (time.time() - now) / (size + 1), "sec")
