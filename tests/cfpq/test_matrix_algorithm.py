import networkx as nx
from pyformlang.cfg import CFG, Variable

import project.cfpq as cfpq


def test_simple():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )

    cfg = CFG.from_text(
        """
    S -> A S1
    S1 -> B C
    A -> a
    B -> b
    C -> c"""
    )

    expected = {
        (0, Variable("A"), 1),
        (1, Variable("B"), 2),
        (2, Variable("C"), 3),
        (1, Variable("S1"), 3),
        (0, Variable("S"), 3),
    }
    res = cfpq.matrix(gr, cfg)
    assert expected == res


def test_extra_graph():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )

    cfg = CFG.from_text(
        """
    S -> B C
    B -> b
    C -> c"""
    )

    expected = {(1, Variable("B"), 2), (2, Variable("C"), 3), (1, Variable("S"), 3)}
    res = cfpq.matrix(gr, cfg)
    assert expected == res


def test_extra_query():
    gr = nx.MultiDiGraph([(0, 1, {"label": "a"}), (1, 2, {"label": "b"})])

    cfg = CFG.from_text(
        """
    S -> B C
    B -> b
    C -> c"""
    )

    expected = {(1, Variable("B"), 2)}
    res = cfpq.matrix(gr, cfg)
    assert expected == res


def test_with_start_final_and_var():
    gr = nx.MultiDiGraph(
        [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    )

    cfg = CFG.from_text(
        """
    S -> A S1
    S1 -> B C
    A -> a
    B -> b
    C -> c"""
    )

    expected = {(0, Variable("S"), 3)}
    res = cfpq.matrix(gr, cfg, {0}, {3}, Variable("S"))
    assert expected == res
