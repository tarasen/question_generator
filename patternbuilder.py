from operator import itemgetter

from cytoolz import frequencies

from _models.pattern import Pattern
from _models.rule_item import RuleItem
from _models.sentence import Sentence
from lib_ex.fizzle import pick_one
from lib_ex.ftools import pluck_attr
from settings import Settings


class PatternBuilder:
    def __init__(self, sentence: Sentence, question: Sentence):
        self.sentence = sentence
        self.question = question

        self.pattern = [RuleItem(Settings.PUNCT_KEY, w.word) if w.tag == 'PNCT' else None for w in question]
        self.arr = question[:-1]
        self.sent = sentence[:-1]

    @property
    def key(self):
        return self.sentence.key

    def find_copy(self):
        for qword in self.arr.copy():
            for word in (w for w in self.sent if w.word == qword.word and w.tag == qword.tag):
                self.pattern[qword.number] = RuleItem(Settings.COPY_KEY, word.number, morph=qword.tag)
                self.sent.remove(word)
                self.arr.remove(qword)
                break

    def find_rule(self):
        for qword in self.arr.copy():
            for word in (w for w in self.sent if w.lemma == qword.lemma):
                self.pattern[qword.number] = RuleItem(Settings.RULE_KEY, word.number, (word.tag, qword.tag))
                self.sent.remove(word)
                self.arr.remove(qword)
                break

    def find_question(self):
        found = False
        for qword in [q for q in self.arr if q.word in Settings.russian_question_words]:
            self.pattern[qword.number] = RuleItem(Settings.QUESTION_KEY, qword.word)
            self.arr.remove(qword)
            found = True

        if not found:
            return

        for qword in [q for q in self.arr if q.word in Settings.russian_hard_questions]:
            self.pattern[qword.number] = RuleItem(Settings.QUESTION_WORD_KEY, qword.word)
            self.arr.remove(qword)

    def find_tag_error(self, questions):
        for qword in self.arr.copy():
            for word in (w for w in self.sent if w.word == qword.word and w.tag != qword.tag):
                try:
                    vars = [w for qu in questions + [self.sentence] for w in qu if w.word == word.word]
                except TypeError:
                    print(word, qword)
                    pass
                fq = frequencies(pluck_attr('tag', vars))
                tag = max(fq.items(), key=itemgetter(1))[0]
                var = next(v for v in vars if v.tag == tag)
                word.base = var
                qword.base = var

                self.pattern[qword.number] = RuleItem(Settings.COPY_KEY, word.number, morph=word.tag)
                self.sent.remove(word)
                self.arr.remove(qword)
                break

    def find_leave_token(self):
        for qword in self.arr.copy():
            if qword.tag in ['PNCT', 'PREP'] or qword.lemma in ['быть']:
                self.pattern[qword.number] = RuleItem(Settings.NEW_TOKEN_KEY, qword.word)
                self.arr.remove(qword)

    def find_wrong_tokens(self, mc):
        def try_upd(w1, w2):
            try:
                w2.base = mc.get_wordform(w1.word, w1.tag, wanted_word=w2.word)
            except StopIteration:
                return False
            return True

        for qword in self.arr.copy():
            word = pick_one(qword.word, pluck_attr('word', self.sent))
            if word[0] > 2:
                continue  # damerau value

            word = next(s for s in self.sent if s.word == word[1])

            if not (try_upd(word, qword) or try_upd(qword, word)):
                continue

            assert word.lemma == qword.lemma

            self.pattern[qword.number] = RuleItem(Settings.RULE_KEY, word.number, (word.tag, qword.tag))
            self.sent.remove(word)
            self.arr.remove(qword)

    @property
    def is_valid(self):
        return all(p is not None for p in self.pattern)

    def build(self):
        return Pattern(self.pattern, pluck_attr('tag', self.sentence), pluck_attr('tag', self.question),
                       [RuleItem(Settings.ANSWER_KEY, s.number, morph=s.tag) for s in self.sent])
