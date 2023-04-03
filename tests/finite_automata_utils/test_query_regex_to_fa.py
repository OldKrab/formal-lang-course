import project.finite_automata_utils as fa_utils
from pyformlang.finite_automaton import EpsilonNFA
import pytest


def test_query_to_one_path():
    fa = EpsilonNFA()
    fa.add_transition(0, "a", 1)
    fa.add_transition(1, "b", 2)
    fa.add_transition(2, "c", 3)
    fa.add_start_state(0)
    fa.add_final_state(3)
    query = "abc"
    pairs = fa_utils.query_regex_to_fa(fa, query)
    assert len(pairs) == 1
    assert (0, 3) in pairs


def test_query_with_multiple_starts():
    fa = EpsilonNFA()
    fa.add_transition(0, "a", 3)
    fa.add_transition(1, "b", 3)
    fa.add_transition(2, "c", 3)
    fa.add_transition(3, "d", 4)
    fa.add_start_state(0)
    fa.add_start_state(1)
    fa.add_start_state(2)
    fa.add_final_state(4)
    query = "(ad|cd)"
    pairs = fa_utils.query_regex_to_fa(fa, query)
    assert len(pairs) == 2
    assert (0, 4) in pairs
    assert (2, 4) in pairs


def test_query_with_multiple_finals():
    fa = EpsilonNFA()
    fa.add_transition(0, "a", 1)
    fa.add_transition(1, "b", 2)
    fa.add_transition(1, "c", 3)
    fa.add_transition(1, "d", 4)
    fa.add_start_state(0)
    fa.add_final_state(2)
    fa.add_final_state(3)
    fa.add_final_state(4)
    query = "(ab|ad)"
    pairs = fa_utils.query_regex_to_fa(fa, query)
    assert len(pairs) == 2
    assert (0, 2) in pairs
    assert (0, 4) in pairs


def test_query_with_loops():
    fa = EpsilonNFA()
    fa.add_transition(0, "a", 1)
    fa.add_transition(1, "b", 1)
    fa.add_transition(0, "c", 2)
    fa.add_transition(2, "d", 2)
    fa.add_transition(0, "e", 3)
    fa.add_transition(3, "f", 3)
    fa.add_start_state(0)
    fa.add_final_state(1)
    fa.add_final_state(2)
    fa.add_final_state(3)
    query = "(abbb|cddd)"
    pairs = fa_utils.query_regex_to_fa(fa, query)
    assert len(pairs) == 2
    assert (0, 1) in pairs
    assert (0, 2) in pairs
