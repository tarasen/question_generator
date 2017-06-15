from logging import getLogger, ERROR
from typing import List, Dict

import rapidjson
from cytoolz import sliding_window
from flask import Flask, request
from werkzeug.serving import WSGIRequestHandler

from morph_service.tokenizer import Tokenizer
from morph_service.viterbi import Viterbi
from morph_service.word_token import WordItem

log = getLogger('werkzeug')
log.setLevel(ERROR)

app = Flask(__name__)


class MorphService:
    def __init__(self, corpora):
        self.__viterbi = Viterbi(corpora)
        self.__tokenizer = Tokenizer()

    @property
    def viterbi(self) -> Viterbi:
        return self.__viterbi

    @viterbi.setter
    def viterbi(self, value: Viterbi):
        self.__viterbi = value

    @property
    def tokenizer(self) -> Tokenizer:
        return self.__tokenizer

    @tokenizer.setter
    def tokenizer(self, value: Tokenizer):
        self.__viterbi = value

    def _tokenize(self, sentence: str) -> List[str]:
        fixed = self.tokenizer.fix_text(sentence)
        return self.tokenizer.tokenize(fixed)

    def _parse(self, tokens: List[str]) -> List[WordItem]:
        return self.viterbi.parse_sentence(tokens)

    def parse(self, sentence: str) -> List[WordItem]:
        return self._parse(self._tokenize(sentence))

    def unigramm(self, word: str, lexeme: bool) -> List[WordItem]:
        return self.viterbi.morphy(word, lexeme)

    def prob(self, sentence:List[Dict[str, str]]):
        x = []
        for pair in sliding_window(2, [{'tag':Viterbi.START_SYMBOL}]+sentence+[{'tag':Viterbi.END_SYMBOL}]):
            x.append(self.viterbi.prob(pair[0]['tag'], pair[1]['tag']))
        import statistics
        return {'mean':statistics.mean(x), 'harmonic_mean':statistics.harmonic_mean(x), 'median':statistics.median(x),
                'pstdev':statistics.pstdev(x), 'stdev':statistics.stdev(x), 'variance':statistics.variance(x),
                'pvariance':statistics.pvariance(x)}
        # return x ** (1/(len(sentence)+2))

service = MorphService("c:/temp/12/corpora.txt")


@app.route('/omonimy', methods=['GET'])
def omonimy():
    data = service.parse(request.args.get('sentence'))

    return rapidjson.dumps([word.as_dict() for word in data], ensure_ascii=False), 200, {
        'Content-Type': 'application/json; charset=utf-8'}


@app.route('/prob', methods=['GET', 'POST'])
def prob():
    body = rapidjson.loads(request.get_json(silent=True, force=True) or '')
    sentence = body['sentence']

    return rapidjson.dumps(service.prob(sentence)), 200, {
               'Content-Type': 'application/json; charset=utf-8'}

@app.route('/morphy', methods=['GET'])
def morphy():
    word = request.args.get('word')
    lexeme = bool(request.args.get('lexeme', False))
    data = service.unigramm(word, lexeme)

    return rapidjson.dumps([word.as_dict() for word in data], ensure_ascii=False), 200, {
        'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    PORT = 7419
    print('ready to serve at',PORT)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(threaded=True, debug=False, port=PORT)
