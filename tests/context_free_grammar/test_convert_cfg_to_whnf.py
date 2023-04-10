from pyformlang.cfg import CFG, Production, Terminal, Variable
from project.context_free_grammar import convert_cfg_to_wcnf


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_simple():
    cfg = CFG.from_text("S -> a | b")
    actual = convert_cfg_to_wcnf(cfg)
    assert actual.terminals == {Terminal("a"), Terminal("b")}
    assert actual.variables == {Variable("S")}
    assert actual.start_symbol == Variable("S")
    assert actual.productions == {
        Production(Variable("S"), [Variable("a")]),
        Production(Variable("S"), [Variable("b")]),
    }


def test_unit_productions():
    cfg = CFG.from_text(
        """
        S -> A
        A -> B
        B -> a
        """
    )
    actual = convert_cfg_to_wcnf(cfg)
    assert actual.terminals == {Terminal("a")}
    assert actual.variables == {Variable("S")}
    assert actual.start_symbol == Variable("S")
    assert actual.productions == {
        Production(Variable("S"), [Variable("a")]),
    }


def test_unreachable_symbols():
    cfg = CFG.from_text(
        """
        S -> A
        A -> a
        B -> a
        """
    )
    actual = convert_cfg_to_wcnf(cfg)
    assert actual.terminals == {Terminal("a")}
    assert actual.variables == {Variable("S")}
    assert actual.start_symbol == Variable("S")
    assert actual.productions == {
        Production(Variable("S"), [Variable("a")]),
    }


def test_productions_with_more_2_symbols():
    cfg = CFG.from_text(
        """
        S -> A B C
        A -> a
        B -> C
        C -> b
        """
    )
    actual = convert_cfg_to_wcnf(cfg)
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
