import atexit
from itertools import starmap

import rapidjson
from requests import session as r_session

__all__ = ['HttpSession']

_session = r_session()


@atexit.register
def __clean_up():
    _session.close()


class HttpSession:
    def __init__(self, base: str):
        self.base = base.rstrip('/')

    def get(self, relative: str, **kwargs):
        path = self.base + '/' + relative.lstrip('/')
        if kwargs:
            path += '?' + '&'.join(starmap(lambda k, v: f'{k}={v}', kwargs.items()))
        return _session.get(path)

    def post(self, relative: str, **kwargs):
        path = self.base + '/' + relative.lstrip('/')
        return _session.post(path, json=rapidjson.dumps(kwargs, ensure_ascii=False))
