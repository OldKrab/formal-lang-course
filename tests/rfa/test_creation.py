import os
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
from sympy.abc import V
from project.ecfg import ECFG
from project.rfa import RFA
from tests.ecfg.test_creation import (
    assert_ecfg_equals_to_default,
    default_cfg,
    default_file_name,
    default_text,
)


def setup_module(module):
    with open(default_file_name(), "w") as file:
        file.write(default_text())
    pass


def teardown_module(module):
    os.remove(default_file_name())


def assert_rfa_equals_to_default(rfa: RFA):
    assert Regex("a* S | A B").to_epsilon_nfa() == rfa.fa_dict[Variable("S")]
    assert Regex("a b").to_epsilon_nfa() == rfa.fa_dict[Variable("A")]
    assert Regex("c").to_epsilon_nfa() == rfa.fa_dict[Variable("B")]
    assert rfa.fa_dict.keys() == {Variable("S"), Variable("A"), Variable("B")}


def test_from_text():
    assert_rfa_equals_to_default(RFA.from_text(default_text()))


def test_from_file():
    assert_rfa_equals_to_default(RFA.from_file(default_file_name()))


def test_from_cfg():
    assert_rfa_equals_to_default(RFA.from_cfg(default_cfg()))


def test_from_ecfg():
    assert_rfa_equals_to_default(RFA.from_ecfg(ECFG.from_cfg(default_cfg())))
