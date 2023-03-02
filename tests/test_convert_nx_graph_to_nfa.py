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
    assert nfa.accepts(["a"])
    assert nfa.accepts(["b"])
    assert nfa.accepts(["c"])
    assert nfa.accepts(["a", "b", "c"])
    assert nfa.accepts(["b", "c"])
    assert not nfa.accepts(["d"])
    assert not nfa.accepts(["a", "b", "d"])
    assert not nfa.accepts(["a", "b", "c", "d"])


def test_cycle_graph_all_start_final():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 0, {"label": "c"})]
    )
    nfa = convert_nx_graph_to_nfa(gr)
    assert nfa.accepts(["a"])
    assert nfa.accepts(["b"])
    assert nfa.accepts(["c"])
    assert nfa.accepts(["a", "b", "c"])
    assert nfa.accepts(["b", "c", "a"])
    assert nfa.accepts(["a", "b", "c", "a", "b", "c", "a"])
    assert not nfa.accepts(["a", "b", "c", "a", "b", "c", "c"])


def test_graph_with_loop_edge_all_start_final():
    gr = nx.MultiDiGraph([(0, 1, {"label": "a"}), (1, 1, {"label": "b"})])
    nfa = convert_nx_graph_to_nfa(gr)
    assert nfa.accepts(["a"])
    assert nfa.accepts(["b"])
    assert nfa.accepts(["b", "b"])
    assert nfa.accepts(["a", "b", "b", "b"])
    assert not nfa.accepts(["a", "b", "b", "a"])


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
    assert nfa.accepts(["a"])
    assert nfa.accepts(["d"])
    assert nfa.accepts(["d", "d"])
    assert nfa.accepts(["a", "b", "c", "d", "d"])
    assert not nfa.accepts(["b"])
    assert not nfa.accepts(["b", "c"])


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
    assert nfa.accepts(["a"])
    assert nfa.accepts(["a", "b", "c"])
    assert nfa.accepts(["d"])
    assert nfa.accepts(["d", "d"])
    assert nfa.accepts(["a", "b", "c", "d", "d"])
    assert nfa.accepts(["b", "c", "d"])
    assert not nfa.accepts(["a", "b"])
    assert not nfa.accepts(["b"])


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
    assert nfa.accepts(["a", "b"])
    assert not nfa.accepts(["d"])
    assert not nfa.accepts(["d", "d"])
    assert not nfa.accepts(["a", "b", "c", "d", "d"])
    assert not nfa.accepts(["b", "c", "d"])
    assert not nfa.accepts(["a"])
    assert not nfa.accepts(["b"])
    assert not nfa.accepts(["a", "b", "c"])
