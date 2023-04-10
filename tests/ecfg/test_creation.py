import os
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.regular_expression import Regex
from sympy.abc import V
from project.ecfg import ECFG


def setup_module(module):
    with open(default_file_name(), "w") as file:
        file.write(default_text())
    pass


def teardown_module(module):
    os.remove(default_file_name())


def assert_ecfg_equals_to_default(ecfg: ECFG):
    assert {Variable("S"), Variable("A"), Variable("B")} == ecfg.variables
    assert {Terminal("a"), Terminal("b"), Terminal("c")} == ecfg.terminals
    assert Variable("S") == ecfg.start_symbol
    assert (
        Regex("a* S | A B").to_epsilon_nfa()
        == ecfg.productions[Variable("S")].to_epsilon_nfa()
    )
    assert (
        Regex("a b").to_epsilon_nfa()
        == ecfg.productions[Variable("A")].to_epsilon_nfa()
    )
    assert (
        Regex("c").to_epsilon_nfa() == ecfg.productions[Variable("B")].to_epsilon_nfa()
    )


def default_text():
    return """
S -> a* S
S -> A B
A -> a b
B -> c
    """


def default_file_name():
    return "test.txt"


def default_cfg():
    return CFG.from_text(default_text())


def test_from_text():
    assert_ecfg_equals_to_default(ECFG.from_text(default_text()))


def test_from_file():
    assert_ecfg_equals_to_default(ECFG.from_file(default_file_name()))


def test_from_cfg():
    assert_ecfg_equals_to_default(ECFG.from_cfg(default_cfg()))
