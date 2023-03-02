import pytest
from project.graph_utils import *  # on import will print something from __init__ file


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_simple_graph_all_start_final():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )
    nfa = convert_nx_graph_to_nfa(gr)
    assert nfa.accepts("a")
    assert nfa.accepts("b")
    assert nfa.accepts("c")
    assert nfa.accepts("abc")
    assert nfa.accepts("bc")
    assert not nfa.accepts("d")
    assert not nfa.accepts("abd")
    assert not nfa.accepts("abcd")


def test_cycle_graph_all_start_final():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 0, {"label": "c"})]
    )
    nfa = convert_nx_graph_to_nfa(gr)
    assert nfa.accepts("a")
    assert nfa.accepts("b")
    assert nfa.accepts("c")
    assert nfa.accepts("abc")
    assert nfa.accepts("bca")
    assert nfa.accepts("abcabca")
    assert not nfa.accepts("abcabcc")


def test_graph_with_loop_edge_all_start_final():
    gr = nx.MultiDiGraph([(0, 1, {"label": "a"}), (1, 1, {"label": "b"})])
    nfa = convert_nx_graph_to_nfa(gr)
    assert nfa.accepts("a")
    assert nfa.accepts("b")
    assert nfa.accepts("bb")
    assert nfa.accepts("abbb")
    assert not nfa.accepts("abba")


def test_graph_with_set_start_states():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (3, 3, {"label": "d"}),
        ]
    )
    nfa = convert_nx_graph_to_nfa(gr, [0, 3])
    assert nfa.accepts("a")
    assert nfa.accepts("d")
    assert nfa.accepts("dd")
    assert nfa.accepts("abcdd")
    assert not nfa.accepts("b")
    assert not nfa.accepts("bc")


def test_graph_with_set_final_states():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (3, 3, {"label": "d"}),
        ]
    )
    nfa = convert_nx_graph_to_nfa(gr, None, [1, 3])
    assert nfa.accepts("a")
    assert nfa.accepts("abc")
    assert nfa.accepts("d")
    assert nfa.accepts("dd")
    assert nfa.accepts("abcdd")
    assert nfa.accepts("bcd")
    assert not nfa.accepts("ab")
    assert not nfa.accepts("b")


def test_graph_with_set_start_and_final_states():
    gr = nx.MultiDiGraph(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "c"}),
            (3, 3, {"label": "d"}),
        ]
    )
    nfa = convert_nx_graph_to_nfa(gr, [0], [2])
    assert nfa.accepts("ab")
    assert not nfa.accepts("d")
    assert not nfa.accepts("dd")
    assert not nfa.accepts("abcdd")
    assert not nfa.accepts("bcd")
    assert not nfa.accepts("a")
    assert not nfa.accepts("b")
    assert not nfa.accepts("abc")
