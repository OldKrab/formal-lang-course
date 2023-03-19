from pyformlang.finite_automaton import EpsilonNFA
import pytest

# on import will print something from __init__ file
import os

from project.finite_automata_utils import find_reachable_in_fa_from_any


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_simple_path():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 3), (3, "b", 4), (4, "a", 3)])

    query = "aba"
    actual = find_reachable_in_fa_from_any(fa, query, [1])
    excepted = {3}
    assert actual == excepted


def test_loop():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 3), (3, "b", 4), (4, "a", 3)])

    query = "(ab?)+"
    actual = find_reachable_in_fa_from_any(fa, query, [1])
    excepted = {3, 4}
    assert actual == excepted


def test_fork():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 2), (2, "b", 3), (1, "a", 4), (4, "c", 5)])

    query = "ab"
    actual = find_reachable_in_fa_from_any(fa, query, [1])
    excepted = {3}
    assert actual == excepted


def test_multiple_starts():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 2), (2, "b", 3), (4, "a", 5), (5, "b", 6)])

    query = "ab"
    actual = find_reachable_in_fa_from_any(fa, query, [1, 4])
    excepted = {3, 6}
    assert actual == excepted
