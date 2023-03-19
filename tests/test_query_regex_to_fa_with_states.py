import project.finite_automata_utils as fa_utils
from pyformlang.finite_automaton import EpsilonNFA
import networkx as nx
import pytest


def test_query_to_one_path():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
        ]
    )
    query = "abc"
    pairs = fa_utils.query_regex_to_fa_with_states(gr, query, {0}, {3})
    assert len(pairs) == 1
    assert (0, 3) in pairs


def test_query_with_multiple_starts():
    gr = nx.MultiDiGraph(
        [
            (0, 3, {"label": "a"}),
            (1, 3, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (3, 4, {"label": "d"}),
        ]
    )
    query = "(ad|cd)"
    pairs = fa_utils.query_regex_to_fa_with_states(gr, query, {0, 1, 2}, {4})
    assert len(pairs) == 2
    assert (0, 4) in pairs
    assert (2, 4) in pairs


def test_query_with_multiple_finals():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (1, 3, {"label": "c"}),
            (1, 4, {"label": "d"}),
        ]
    )
    query = "(ab|ad)"
    pairs = fa_utils.query_regex_to_fa_with_states(gr, query, {0}, {2, 3, 4})
    assert len(pairs) == 2
    assert (0, 2) in pairs
    assert (0, 4) in pairs


def test_query_with_loops():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 1, {"label": "b"}),
            (0, 2, {"label": "c"}),
            (2, 2, {"label": "d"}),
            (0, 3, {"label": "e"}),
            (3, 3, {"label": "f"}),
        ]
    )
    query = "(abbb|cddd)"
    pairs = fa_utils.query_regex_to_fa_with_states(gr, query, {0}, {1, 2, 3})
    assert len(pairs) == 2
    assert (0, 1) in pairs
    assert (0, 2) in pairs
