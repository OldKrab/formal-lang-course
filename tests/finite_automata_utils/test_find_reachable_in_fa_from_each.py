from pyformlang.finite_automaton import EpsilonNFA
import pytest

# on import will print something from __init__ file
import os

from project.finite_automata_utils import find_reachable_in_fa_from_each


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_multiple_starts():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 2), (2, "b", 3), (4, "a", 5), (5, "b", 6)])

    query = EpsilonNFA()
    query.add_transitions([(0, "a", 1), (1, "b", 2)])
    query.add_start_state(0)
    query.add_final_state(2)
    actual = find_reachable_in_fa_from_each(fa, query, [1, 4])
    excepted = {1: {3}, 4: {6}}
    assert actual == excepted


def test_multiple_starts_one_final():
    fa = EpsilonNFA()
    fa.add_transitions([(1, "a", 2), (2, "b", 3), (4, "a", 5), (5, "b", 3)])

    query = EpsilonNFA()
    query.add_transitions([(0, "a", 1), (1, "b", 2)])
    query.add_start_state(0)
    query.add_final_state(2)
    actual = find_reachable_in_fa_from_each(fa, query, [1, 4])
    excepted = {1: {3}, 4: {3}}
    assert actual == excepted
