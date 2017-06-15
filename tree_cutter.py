from copy import deepcopy
from typing import List, Tuple, Iterator

from cytoolz import get

from _models.sentence import Sentence
from _models.syntax_item import SyntaxItem


class TreeCutter:
    def __init__(self, sentence: Sentence, check_root=True):
        self.sentence = sentence
        self.edges = []
        self.root = set()
        self.check_root = check_root

        for word in self.sentence[:-1]:
            if word.is_root:
                self.root.add(word.number)
            else:
                self.edges.append((word.head, word.number))

    def __neighbors(self, node):
        return [x for x in self.edges if node in x]

    def __find_all_trees(self, all_nodes, tree_length):
        exhausted_node = set()
        used_node = set()
        used_edge = set()
        current_edge_groups = []

        def finish_all_trees(remaining_length, edge_group, edge_position):
            while edge_group < len(current_edge_groups):
                edges = current_edge_groups[edge_group]
                while edge_position < len(edges):
                    edge = edges[edge_position]
                    edge_position += 1
                    node1, node2 = edge
                    if node1 in exhausted_node or node2 in exhausted_node:
                        continue
                    node = node1
                    if node1 in used_node:
                        if node2 in used_node:
                            continue
                        else:
                            node = node2
                    used_node.add(node)
                    used_edge.add(edge)
                    current_edge_groups.append(self.__neighbors(node))
                    if remaining_length == 1:
                        yield (used_node, used_edge)
                    else:
                        yield from finish_all_trees(remaining_length - 1, edge_group, edge_position)
                    current_edge_groups.pop()
                    used_edge.remove(edge)
                    used_node.remove(node)
                edge_position = 0
                edge_group += 1

        for node in all_nodes:
            used_node.add(node)
            current_edge_groups.append(self.__neighbors(node))
            yield from finish_all_trees(tree_length, 0, 0)
            current_edge_groups.pop()
            used_node.remove(node)
            exhausted_node.add(node)

    def __iter__(self) -> Iterator[Tuple[List[SyntaxItem], Iterator[int]]]:
        links = []
        nd = range(1, len(self.edges))
        for i in range(1, len(self.edges)):
            for nodes, e in self.__find_all_trees(nd, i):
                if nodes and (not self.check_root or nodes & self.root):
                    arr = []
                    d = {-1: -1}
                    for pos, j in enumerate(nodes):
                        w = deepcopy(self.sentence[j])
                        w.number = pos
                        d[j] = pos
                        arr.append(w)
                        links.append(j)
                    for w in arr:
                        w.head = get(w.head, d, -1)
                    last = deepcopy(self.sentence[-1])
                    last.number = len(nodes)

                    links.append(last.number)
                    yield arr + [last], links
                    links = []
        yield list(self.sentence), range(len(self.sentence))
