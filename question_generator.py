# -*- coding: utf-8 -*-

from collections import defaultdict
from time import time
from typing import List, Tuple

import networkx
from cytoolz import groupby, pluck, first, drop
from networkx.readwrite import json_graph
from tqdm import tqdm

from _models.pattern import Pattern
from _models.rule_item import RuleItem
from _models.sentence import Sentence, DummySentence
from _web_clients.morph_client import MorphClient
from db_adapter import DbAdapter
from lib_ex.ftools import boolfilter, pluck_attr
from morph_service.word_token import WordItem
from patternbuilder import PatternBuilder
from sent_transformer import Transformer
from sentence_factory import SentenceFactory
from settings import Settings
from tag_normalizer import TagNormalizer
from tree_cutter import TreeCutter


class QuestionGenerator:
    def __init__(self, db_adapter: DbAdapter):
        self.mc = MorphClient()
        self.db_adapter = db_adapter
        self.norm = TagNormalizer()
        self.sf = SentenceFactory(self.mc, self.norm)
        self.rules = {}

    def create_pattern(self, sentence, question, all_questions):
        p = PatternBuilder(sentence, question)

        p.find_copy()
        p.find_tag_error(all_questions)
        p.find_rule()
        p.find_question()
        p.find_leave_token()
        p.find_wrong_tokens(self.mc)

        return p.build() if p.is_valid else None

    def add(self, sentence, questions, graph=None):
        print(sentence.original)

        key = sentence.key

        patterns = [(self.create_pattern(sentence, q, questions), q) for q in questions]

        if key != sentence.key:
            self.sf.resyntax(sentence)
            for q in questions:
                self.sf.resyntax(q)

        all_pattens = defaultdict(list)
        all_pattens[sentence].extend(patterns)

        if graph:
            trans = Transformer(sentence, graph, self.mc)
            for p, q in patterns:
                if not p:
                    continue
                try:
                    extends = groupby(lambda k: k[0].original, trans.process_question(q, p))
                except TimeoutError:
                    print('sent timeout:', q)
                    continue

                for pairs in extends.values():
                    sent = first(pluck(0, pairs))
                    quests = list(pluck(1, pairs))
                    all_pattens[sent].extend(
                        (self.create_pattern(sent, q, quests), 1) for q in quests)

        for sent, pts in all_pattens.items():
            pts = list(boolfilter(pluck(0, pts)))
            json_key, sent_graph = self.sf.get_json(sent.key)

            json_key['node_str'] = '|'.join(sorted(pluck('id', json_key['nodes'])))
            json_key['links_str'] = '|'.join(sorted(pluck('type', json_key['links'])))

            vars = list(self.db_adapter.find(node_str=json_key['node_str'], links_str=json_key['links_str']))
            if not vars:
                self.db_adapter.add(patterns=list(map(lambda r: r.as_dict(), pts)), **json_key)
            else:
                for v in vars:
                    if networkx.is_isomorphic(json_graph.node_link_graph(v), sent_graph):
                        exist_pattern = list(map(Pattern.from_dict, v['patterns']))
                        extended = False
                        for p in pts:
                            if all(p != ep for ep in exist_pattern):
                                exist_pattern.append(p)
                                extended = True
                        if extended:
                            self.db_adapter.update(v['_id'], patterns=list(map(lambda r: r.as_dict(), exist_pattern)))

    def find(self, words: Sentence or str):
        if isinstance(words, str):
            words = self.sf.parse(words)

        key = words.key
        json_key, sent_graph = self.sf.get_json(key)

        node_str = '|'.join(sorted(pluck('id', json_key['nodes'])))
        links_str = '|'.join(sorted(pluck('type', json_key['links'])))

        vars = list(self.db_adapter.find(node_str=node_str, links_str=links_str))

        if not vars:
            return None

        def apply_rule(circle: RuleItem, sentence: Sentence, pattern: Pattern):
            if circle.tag == Settings.COPY_KEY:
                founds = [w for w in sentence if w.tag == circle.morph]
                if len(founds) == 1:
                    return founds[0]
                assert len(founds) == 1 and founds[0].number == circle.link

            if circle.tag in [Settings.QUESTION_KEY, Settings.NEW_TOKEN_KEY, Settings.PUNCT_KEY]:
                return WordItem(circle.link, None, pattern.quest_tags[list(pattern).index(circle)], 1)

            if circle.tag == Settings.RULE_KEY:
                founds = [w for w in sentence if w.tag == circle.rule[0]]
                if len(founds) == 1:
                    return self.mc.get_wordform(founds[0].word, *circle.rule)
                assert len(founds) == 1 and founds[0].number == circle.link

            if circle.tag == Settings.ANSWER_KEY:
                founds = [w for w in words if w.tag == circle.morph]
                if len(founds) == 1:
                    return founds[0]
                assert len(founds) == 1 and founds[0].number == circle.link

        for v in vars:
            if networkx.is_isomorphic(json_graph.node_link_graph(v), sent_graph):
                questions = []
                for pattern in map(Pattern.from_dict, v['patterns']):
                    q = DummySentence([apply_rule(c, words, pattern) for c in pattern])
                    a = DummySentence([apply_rule(c, words, pattern) for c in pattern.answer] + [words[-1]])
                    questions.append((q, a))
                return questions
        return None

    def get_questions(self, sent: Sentence or str) -> List[Tuple[DummySentence, DummySentence]]:
        if isinstance(sent, str):
            sent = self.sf.parse(sent)

        questions = []
        for s, _ in TreeCutter(sent):
            local_sent = Sentence(s)
            quest = self.find(local_sent)
            if quest is not None:
                questions.extend(quest)

        questions.sort(key=lambda q: len(q[0]))
        valid = set()
        for i in range(len(questions)):
            if not any(set(pluck_attr('word', questions[i][0])) <= set(pluck_attr('word', questions[j][0])) for j in range(i + 1, len(questions))):
                valid.add(questions[i])
        return valid or None

    def _read_all(self, path):
        questions = []
        sentences = []

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                sentence = line.strip()
                if sentence == '':
                    yield (sentences, questions)
                    questions = []
                    sentences = []
                elif sentence[-1] != '?':
                    sentences.append(self.sf.parse(sentence))
                else:
                    questions.append(self.sf.parse(sentence))
        if len(sentences) > 0:
            return sentences, questions

    def train(self, path, graph=None):
        graph = graph or networkx.read_gpickle('graph/rules_graph.gpickle')
        dr = 0#21183 // 2 + 433
        for s, q in tqdm(drop(dr, ((sent, q) for s, q in self._read_all(path) for sent in s)), total=21183 - dr):
            self.add(s, q, graph)


if __name__ == '__main__':
    qf = QuestionGenerator(DbAdapter.create_mongo('diploma2', 'patterns'))
    sf = qf.sf

    # sent = sf.parse('Cолнце уходит с небесного свода.')
    #
    # res = qf.get_questions(sent)
    #
    # from pprint import pprint
    # pprint(res)
    #
    # exit(0)
#     qf.train("c:/temp/12/qustions_corpora.txt")
#     exit(0)
#
#     txt = """В одном лесу жила была Мышь.
#     Была она маленькая-премаленькая, но хитрая-прехитрая.
#     она любила немного приукрасить события.
#     это было ей выгодно.
#     Дело было в самый разгар лета.
#     кругом зеленеют травы, цветут цветы.
#     в воздухе летают запахи.
#     В один такой прекрасный летний день пошла Мышь погулять по полю.
#     решила она насобирать пшеничных колосков.
#     До зимы было далеко.
#     готовиться к ней нужно всё лето.
#     Долго бродила Мышь.
#     колоски ей не попадались.
#     Она решила расстроиться.
#     Ёжик тащит целую охапку колосков.
#     Мышь хорошо знала Ёжика.
#     снег медленно таял на ее веках.
#     Позволяет строить модель по размеченному корпусу.
#     мама мыла раму.
#     Съешьте ещё этих мягких французских булок.
#     Планета Юпитер видна невооруженным глазом.
#     Быстро склоняется солнце за лес.
#     Cолнце уходит с небесного свода.
#     Деревья в этом парке посадили давным-давно."""
#
#     geo = """К числу важнейших социально-экономических процессов современности относится урбанизация.
# Урбанизация – это рост городов, повышение удельного веса городского населения в стране, регионе, мире, возникновение и развитие все более сложных сетей и систем городов.
# Современная урбанизация как всемирный процесс обладает тремя общими чертами, характерными для большинства стран. Первая черта урбанизации – быстрые темпы роста городского населения, особенно в менее развитых странах. В среднем, городское население ежегодно увеличивается примерно на 60 млн человек. Вторая черта урбанизации – концентрация населения и хозяйства, в основном, в больших городах. Это объясняется, прежде всего, характером производства, усложнением его связей с наукой и образованием. Третья черта урбанизации – «расползание» городов, расширение их территорий. Для современной урбанизации особенно характерен переход от компактного («точечного») города к городским агломерациям.
# Городская агломерация – большой город, вокруг которого развиваются малые города, связанные с ним различными видами связей (экономических, транспортных, культурных и так далее)
# В 1970 г. в мире было всего три городские агломерации с населением свыше 10 млн человек – Токио, Нью-Йорк и Шанхай. В 1990 г. агломераций с населением свыше 10 млн человек стало 12, а к 2000 г. число их возросло до 23. При этом самой крупной агломерацией мира была и остается Токийская. Многие из агломераций трансформируются в более крупные городские образования – мегалополисы.
# Мегалополисы – скопление агломераций и городов, слившихся друг с другом. Мегалополисы уже появились в Японии, и в США. В настоящее время идёт процесс их образования в Европе.
# Несмотря на наличие общих черт урбанизации как всемирного процесса, в разных странах и регионах она имеет свои особенности, которые, прежде всего, находят выражение в различных уровнях и темпах урбанизации. По уровню урбанизации все страны мира подразделяются на три большие группы:
# высокоурбанизированные (доля городского населения свыше 50 %);
# среднеурбанизированные (доля городского населения от 20 до 50 %);
# слабоурбанизированные (доля городского населения ниже 20 %).
# В развитых странах уровень урбанизации в среднем составляет 75 %, а в развивающихся – 41 %. Уровень урбанизации стран показан на рисунке.
# Темпы урбанизации страны во многом зависят от её уровня развития. В большинстве экономически развитых стран, достигших высокого уровня урбанизации, доля городского населения в последнее время растёт сравнительно медленно, а число жителей в столицах и других крупных городах, как правило, даже уменьшается. Многие горожане теперь предпочитают жить не в центрах больших городов, а в пригородах и сельской местности. Но урбанизация продолжает развиваться «вглубь», приобретая новые формы.
# В развивающихся странах, где уровень урбанизации значительно более низкий, она продолжает расти «вширь», а городское население быстро увеличивается. Это явление, получившее в науке наименование «городского взрыва», стало одним из важнейших факторов социально-экономической жизни развивающихся стран. В развивающихся странах сейчас находится также большинство городов-миллионеров и «сверхгородов». Рост населения городов в этих регионах намного опережает их реальное развитие. Он происходит в значительной мере благодаря постоянному «выталкиванию» избыточного сельского населения в крупные города. При этом неимущее население обычно селится на окраинах больших городов, где возникают «пояса нищеты», пояса трущоб. Подобная «трущобная урбанизация» приняла очень большие размеры. Особенно велика здесь (47 %) доля Зарубежной Азии."""
#
#     # smr = Summarizer(sf.mc)
#
#     for line in txt.split('\n'):  # smr.get_summary(txt, 1):
#         sent = sf.parse(line.strip())
#         print(qf.get_questions(sent))
#
#     exit(0)

    g = networkx.read_gpickle('graph/rules_graph.gpickle')

    def process(text, quests):
        sent = sf.parse(text)

        q_sents = []
        for q in quests:
            quest = sf.parse(q)
            q_sents.append(quest)

        qf.add(sent, q_sents, g)


    # process(u'белый камень медленно падал.', [
    #     u'что медленно делал белый камень?',
    #     u'что медленно падало?',
    #     u'какой камень медленно падал?',
    #     u'как падал белый камень?'])

    process(u'белый снег медленно таял.', [
        u'Что медленно таяло?',
        u'Что медленно делал белый снег?',
        u'Какой снег медленно таял?'])

    process(u'Красивая птица быстро летает.', [
        u'Кто быстро летает?',
        u'Что быстро делает красивая птица?',
        u'Какая птица быстро летает?',
        u'Как летает красивая птица?'
    ])

    process(u'Мы скоро будем праздновать.', [
        u'Кто скоро будет праздновать?',
        u'Что мы скоро будем делать?',
        u'Когда мы будем праздновать?'])

    process(u'Деревянный стол стоит у открытого окна.', [
        u'Что стоит у открытого окна?',
        u'Какой стол стоит у открытого окна?',
        u'Что деревянный стол делает у открытого окна?',
        u'У чего стоит деревянный стол?',
        u'У какого окна стоит деревянный стол?'
    ])

    process(u'Давно улетели на юг щебечущие ласточки.', [
        u'Когда улетели на юг щебечущие ласточки?',
        u'Куда давно улетели щебечущие ласточки?',
        u'Кто давно улетел на юг?'
    ])

    process(u'Щебечущие ласточки давно улетели на юг.', [
        u'Когда улетели на юг щебечущие ласточки?',
        u'Куда давно улетели щебечущие ласточки?',
        u'Кто давно улетел на юг?'
    ])
    process(u'На юг давно улетели щебечущие ласточки.', [
        u'Когда улетели на юг щебечущие ласточки?',
        u'Куда давно улетели щебечущие ласточки?',
        u'Кто давно улетел на юг?'
    ])
