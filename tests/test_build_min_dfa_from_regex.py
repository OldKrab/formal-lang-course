import pytest
import project.graph_utils as graph_utils  # on import will print something from __init__ file
import pyformlang.regular_expression


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_simple_regex():
    regex = r"[pl]oopa"
    dfa = graph_utils.build_min_dfa_from_regex(regex)

    assert dfa.accepts("poopa")
    assert dfa.accepts("poopa")
    assert not dfa.accepts("doopa")
    assert not dfa.accepts("loop")
    assert not dfa.accepts("poopaa")


def test_is_min_dfa():
    regex = r"([a-z1-9]+|[1-9]*)(abc|abd)"
    dfa = graph_utils.build_min_dfa_from_regex(regex)

    assert dfa.is_deterministic()
    assert dfa.is_equivalent_to(dfa.minimize())


def test_repeating_regex():
    regex = r"[abc]+"
    dfa = graph_utils.build_min_dfa_from_regex(regex)

    assert dfa.accepts("a")
    assert dfa.accepts("b")
    assert dfa.accepts("c")
    assert dfa.accepts("abbbcaccaacb")
    assert not dfa.accepts("")
    assert not dfa.accepts("abcd")
