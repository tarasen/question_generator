import subprocess
from logging import getLogger, ERROR
from time import sleep

import rapidjson
from cytoolz import take
from flask import Flask, request
from werkzeug.serving import WSGIRequestHandler

from syntax_service.syntax_analyzer import SyntaxAnalyzer

log = getLogger('werkzeug')
log.setLevel(ERROR)

app = Flask(__name__)


def run_win_cmd(cmd, top=2):
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    sleep(5)
    for line in take(top, process.stdout):
        print(line.decode().strip())
    errcode = process.returncode
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)


def init_analyzer():
    try:
        return SyntaxAnalyzer()
    except:
        cmd = """java -cp C:\\temp\\maltparser-1.9.0\\maltparser-1.9.0.jar;C:\\temp\\py4j-0.10.4\\py4j-java\\py4j0.10.4.jar;. MaltGateway syntagrus &"""
        run_win_cmd(cmd)
        return SyntaxAnalyzer()


service = init_analyzer()


@app.route('/parse', methods=['GET', 'POST'])
def parse():
    body = rapidjson.loads(request.get_json(silent=True, force=True) or '')
    sentences = body['sentences']
    return rapidjson.dumps(
        [{**a, 'head': b[0], 'deprel': b[1]} for a, b in zip(sentences, service.build_syntax(sentences))],
        ensure_ascii=False), 200, {
               'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    PORT = 7418
    print('ready to serve at', PORT)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(threaded=True, debug=False, port=PORT)
