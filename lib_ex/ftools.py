from operator import attrgetter
from typing import Iterator


def pluck_attr(attr: str, seq: Iterator):
    return map(attrgetter(attr), seq)


def boolfilter(seq: Iterator):
    return filter(bool, seq)


def starfilter(func, seq):
    return filter(lambda p: func(*p), seq)


def c_plus(item):
    return lambda a: a + item


def c_mul(item):
    return lambda a: a * item


def c_eq(item):
    return lambda a: a == item


def c_lt(item):
    return lambda a: a < item


def c_gt(item):
    return lambda a: a > item


def c_le(item):
    return lambda a: a <= item


def c_ge(item):
    return lambda a: a >= item


def c_in(coll):
    return lambda a: a in coll


def c_contains(item):
    return lambda coll: item in coll
