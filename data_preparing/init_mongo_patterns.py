from itertools import permutations
from operator import itemgetter
from sys import intern

import networkx
import pymongo
import rapidjson
from cytoolz import groupby, cons, pluck, valmap, frequencies
from networkx.readwrite import json_graph
from pymongo import MongoClient
from tqdm import tqdm

from tag_normalizer import TagNormalizer

if __name__ == '__main__':
#     tn = TagNormalizer()
#
#     with open('c:/temp/12/qustions_rules.txt', 'r', encoding='utf-8') as f:
#         rules = rapidjson.loads(f.read())
#
#     rls = {}
#     for rule in tqdm(rules):
#         tagkey = tuple((tn.normalize(k[0]), k[1], intern(k[2])) for k in rule['key'])
#
#         key = [[i, tn.normalize(k[0]), k[1], intern(k[2])] for i, k in enumerate(rule['key'][:-1])]
#         key = sorted(
#             [(k[0], k[1] + '_' + str(i), k[2], k[3]) for x in groupby(itemgetter(1), key).values() for i, k in
#              enumerate(sorted(x, key=itemgetter(0)))], key=itemgetter(0))
#         nx = networkx.DiGraph()
#         nx.add_node('root')
#         key = list(map(tuple, key))
#         edges = {((a[:2], a[3], b[:2]) if a[2] == b[0] else (b[:2], b[3], a[:2])) for a, b in
#                  permutations(cons((-1, 'root', -1, None), key), 2) if a[0] == b[2] or a[2] == b[0]}
#         for e in edges:
#             nx.add_edge(e[2][1], e[0][1], type=e[1])
#
#         data = json_graph.node_link_data(nx)
#         data['node_str'] = '|'.join(sorted(pluck('id', data['nodes'])))
#         data['links_str'] = '|'.join(sorted(pluck('type', data['links'])))
#         patterns = [
#             [{'tag': intern(i['tag']), 'link': i['link'],
#               'rule': i['rule'] and (tn.normalize(i['rule'][0]), tn.normalize(i['rule'][1]))}
#              for i in p] for p in rule['value']]
#         if tagkey in rls:
#             exist = rls[tagkey]
#
#             rls[tagkey] = ({**data, 'patterns': patterns})
#         else:
#             rls[tagkey] = ({**data, 'patterns': patterns})
#
# lk = frequencies(valmap(lambda v: (v['node_str'], v['links_str']), rls).values())

    DB_NAME = 'diploma2'
    client = MongoClient('mongodb://localhost/' + DB_NAME)

    db = client[DB_NAME]

    db.drop_collection('patterns')
    # db.patterns.insert_many(rls.values())
    result = db.patterns.create_index([('links', pymongo.ASCENDING)], unique=False)
    result = db.patterns.create_index([('nodes', pymongo.ASCENDING)], unique=False)
    result = db.patterns.create_index([('node_str', pymongo.ASCENDING)], unique=False)
    result = db.patterns.create_index([('links_str', pymongo.ASCENDING)], unique=False)
    result = db.patterns.create_index([('node_str', pymongo.ASCENDING), ('links_str', pymongo.ASCENDING)], unique=False)
