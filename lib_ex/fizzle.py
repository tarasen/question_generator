import operator
from operator import itemgetter

from cytoolz import topk, compose


def dl_distance(s1, s2,
                return_matrix=False, non_matching_ends=False, transposition=True,
                second_half_discount=False):
    """
    Return DL distance between s1 and s2. Default cost of substitution, insertion, deletion and transposition is 1
    substitutions is list of tuples of characters (what, substituted by what, cost), 
        maximal value of substitution is 2 (ie: cost deletion & insertion that would be otherwise used)
        eg: substitutions=[('a','e',0.4),('i','y',0.3)]
    symetric=True mean that cost of substituting A with B is same as B with A
    returnMatrix=True: the matrix of distances will be returned, if returnMatrix==False, then only distance will be returned
    printMatrix==True: matrix of distances will be printed
    transposition=True (default): cost of transposition is 1. transposition=False: cost of transpositin is Infinity
    """
    if not isinstance(s1, str):
        s1 = str(s1, "utf8")
    if not isinstance(s2, str):
        s2 = str(s2, "utf8")

    from collections import defaultdict
    subs = defaultdict(lambda: 1)  # default cost of substitution is 1

    if non_matching_ends:
        matrix = [[j for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
    else:  # start and end are aligned
        matrix = [[i + j for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
        # matrix |s1|+1 x |s2|+1 big. Only values at border matter
    half1 = len(s1) / 2
    half2 = len(s2) / 2
    for i in range(len(s1)):
        for j in range(len(s2)):
            ch1, ch2 = s1[i], s2[j]
            if ch1 == ch2:
                cost = 0
            else:
                cost = subs[(ch1, ch2)]
            if second_half_discount and (s1 > half1 or s2 > half2):
                deletion_cost, insertion_cost = 0.6, 0.6
            else:
                deletion_cost, insertion_cost = 1, 1

            matrix[i + 1][j + 1] = min([matrix[i][j + 1] + deletion_cost,  # deletion
                                        matrix[i + 1][j] + insertion_cost,  # insertion
                                        matrix[i][j] + cost  # substitution or no change
                                        ])

            if transposition and i >= 1 and j >= 1 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                matrix[i + 1][j + 1] = min([matrix[i + 1][j + 1],
                                            matrix[i - 1][j - 1] + cost])

    return matrix if return_matrix else matrix[-1][-1]


def dl_ratio(s1, s2):
    'returns distance between s1&s2 as number between [0..1] where 1 is total match and 0 is no match'
    try:
        return 1 - (dl_distance(s1, s2)) / (2.0 * max(len(s1), len(s2)))
    except ZeroDivisionError:
        return 0.0


def match_list(s, l):
    '''
    returns list of elements of l with each element having assigned distance from s
    '''
    return ((dl_distance(s, x), x) for x in l)


def pick_N(s, l, num=3):
    ''' picks top N strings from options best matching with s 
        - if num is set then returns top num results instead of default three
    '''

    return topk(num, match_list(s, l), compose(operator.neg, itemgetter(0)))


def pick_one(s, l):
    try:
        return pick_N(s, l, 1)[0]
    except IndexError:
        return None


if __name__ == "__main__":
    # examples:
    misspellings = ["Levenshtain", "Levenstein", "Levinstein", "Levistein", "Levemshtein"]

    print(dl_distance('dayme', 'dayne'))
    print(dl_ratio("Levenshtein", "Levenshtein"))
    print(list(match_list("Levenshtein", misspellings)))
    print(pick_N("Levenshtein", misspellings, 2))
    print(pick_one("Levenshtein", misspellings))
