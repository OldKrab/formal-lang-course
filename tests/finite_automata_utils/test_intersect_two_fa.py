import project.finite_automata_utils as fa_utils
import pytest


def test_simple_intersect():
    lhs = fa_utils.build_min_dfa_from_regex("[bc]")
    rhs = fa_utils.build_min_dfa_from_regex("[ab]")
    res = fa_utils.intersect_two_fa(lhs, rhs)
    assert res.accepts("b")
    assert not res.accepts("a")
    assert not res.accepts("c")


def test_intersect_with_optional():
    lhs = fa_utils.build_min_dfa_from_regex("abc?")
    rhs = fa_utils.build_min_dfa_from_regex("abd?")
    res = fa_utils.intersect_two_fa(lhs, rhs)
    assert res.accepts("ab")
    assert not res.accepts("abc")
    assert not res.accepts("abd")


def test_intersect_with_loops():
    lhs = fa_utils.build_min_dfa_from_regex("[ab]+[de]+")
    rhs = fa_utils.build_min_dfa_from_regex("[ac]+[df]+")
    res = fa_utils.intersect_two_fa(lhs, rhs)
    accepts = ["ad", "aaaaddd"]
    not_accepts = ["ab", "ac", "ae", "af", "bd", "cd"]
    for accept in accepts:
        assert res.accepts(accept)
    for not_accept in not_accepts:
        assert not res.accepts(not_accept)
