from sys import intern
from typing import List, Tuple

class CorporaReader:
    @staticmethod
    def read_opencorpora(path: str, start: str = None, end: str = None) -> List[List[Tuple[str, str]]]:
        tagged_sents = []
        if start and end:
            start, end = [(start, start)], [(end, end)]
        with open(path, 'rt', encoding="utf-8") as f:
            snt = []
            for line in f:
                word = list(map(intern, line.rstrip('\n').split('\t')))
                if len(word) != 3:
                    if len(snt) > 1:
                        if start and end:
                            snt = start + snt + end
                        tagged_sents.append(snt)
                    snt = []
                else:
                    snt.append((word[0], word[2]))
        return tagged_sents
