import operator
from functools import reduce
from itertools import starmap

import rapidjson
from cytoolz import mapcat, concat, sliding_window
from flask import Flask, request
from werkzeug.serving import WSGIRequestHandler

from db_adapter import DbAdapter
from json_reader import JsonWorker
from lib_ex.ftools import boolfilter, starfilter, pluck_attr
from question_generator import QuestionGenerator
from summy import Summarizer

app = Flask(__name__)


class QuestionService:
    def __init__(self, qg: QuestionGenerator):
        self.qg = qg
        self.summy = Summarizer(qg.mc)
        self.__cpd_tags = JsonWorker.read('c:/temp/12/cpd_tags2.json', ('k', 'v'))

    def sent_prob(self, sent):
        def _prob_2(prev: str, nxt: str) -> float:
            return self.__cpd_tags.get((prev, nxt), 1e-10)
        x = [_prob_2(*p) for p in sliding_window(2, ['<S>'] + list(pluck_attr('tag', sent)) + ['</S>'])]

        import statistics
        return {'mean': statistics.mean(x), 'harmonic_mean': statistics.harmonic_mean(x),
                'variance': statistics.variance(x), 'pvariance': statistics.pvariance(x)}

    def qfilter(self, q, a):
        res = True
        if 'NPRO' in pluck_attr('pos', q):
            res = res and all(self.qg.mc.get_lemma(w.word, w.tag) in ['кто', 'что'] for w in q if w.pos == 'NPRO')
        prob = self.sent_prob(q)
        res = res and prob['harmonic_mean'] > 1e-3

        print(q.original)
        print(prob)

        return res

    def get_questions(self, text: str, size: int or float):
        tx = text.lower()
        summary = list(self.summy.get_summary(tx, size))
        questions = list(concat(boolfilter(map(self.qg.get_questions, summary))))
        filtered = starfilter(self.qfilter, questions)

        return [{'question': [w.as_dict() for w in q], 'answer': [w.as_dict() for w in a]} for q, a in filtered]


service = QuestionService(QuestionGenerator(DbAdapter.create_mongo('diploma2', 'patterns')))


@app.route('/questions', methods=['GET'])
def questions():
    text = request.args.get('text')
    count = float(request.args.get('count', 0.99))

    return rapidjson.dumps(service.get_questions(text, count), ensure_ascii=False), 200, {
        'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    PORT = 7421
    print('ready to serve at', PORT)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(threaded=True, debug=False, port=PORT)
