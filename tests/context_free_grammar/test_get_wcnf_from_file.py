import os
from pyformlang.cfg import CFG, Production, Terminal, Variable
from project.context_free_grammar import get_wcnf_from_file


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    actual = get_wcnf_from_file(os.path.join(current_dir, "resources", "cfg1.txt"))
    assert actual.terminals == {Terminal("a"), Terminal("b")}
    assert actual.variables == {
        Variable("S"),
        Variable("A"),
        Variable("B"),
        Variable("C"),
        Variable("C#CNF#1"),
    }
    assert actual.start_symbol == Variable("S")
    assert actual.productions == {
        Production(Variable("S"), [Variable("A"), Variable("C#CNF#1")]),
        Production(Variable("C#CNF#1"), [Variable("B"), Variable("C")]),
        Production(Variable("A"), [Variable("a")]),
        Production(Variable("B"), [Variable("b")]),
        Production(Variable("C"), [Variable("b")]),
    }
