from pyformlang.finite_automaton import EpsilonNFA
import pytest

# on import will print something from __init__ file
import os
import networkx as nx

from project.finite_automata_utils import (
    find_reachable_in_graph_from_any,
    find_reachable_in_graph_from_each,
)


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_loop():
    gr = nx.MultiDiGraph(
        [
            (1, 3, {"label": "a"}),
            (3, 4, {"label": "b"}),
            (4, 3, {"label": "a"}),
        ]
    )
    query = "aba"
    actual = find_reachable_in_graph_from_any(gr, query, [1], [3])
    excepted = {3}
    assert actual == excepted


def test_multiple_starts():
    gr = nx.MultiDiGraph(
        [
            (1, 2, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (4, 5, {"label": "a"}),
            (5, 6, {"label": "b"}),
        ]
    )
    query = "ab"
    actual = find_reachable_in_graph_from_any(gr, query, [1, 4], [6])
    excepted = {6}
    assert actual == excepted


def test_multiple_starts_for_each():
    gr = nx.MultiDiGraph(
        [
            (1, 2, {"label": "a"}),
            (2, 3, {"label": "b"}),
            (2, 4, {"label": "b"}),
            (5, 6, {"label": "a"}),
            (6, 3, {"label": "b"}),
            (6, 7, {"label": "b"}),
        ]
    )
    query = "ab"
    actual = find_reachable_in_graph_from_each(gr, query, [1, 5], [4, 7])
    excepted = {1: {4}, 5: {7}}
    assert actual == excepted
