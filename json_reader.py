from sys import intern
from typing import Tuple, Dict

import json
import rapidjson


class JsonWorker:
    @staticmethod
    def read(path: str, kv: Tuple[str, str] = None, rjson: bool = True):
        js_ser = rapidjson if rjson else json
        with open(path, 'r', encoding='utf-8') as f:
            line = js_ser.loads(f.read())
        if kv:
            key, value = kv
            return {tuple(map(intern, jobj[key])): jobj[value] for jobj in line}
        else:
            return line

    @staticmethod
    def write(path: str, data: Dict, kv: Tuple[str, str] = None):
        if kv:
            key, value = kv

            def _remap_keys(mapping):
                return [{key: k, value: v} for k, v in mapping.items()]

            data_dict = rapidjson.dumps(_remap_keys(data), ensure_ascii=False)
        else:
            data_dict = rapidjson.dumps(data, ensure_ascii=False)
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(data_dict)
