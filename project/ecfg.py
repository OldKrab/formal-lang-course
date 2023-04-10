from typing import AbstractSet, Any, Dict, Set
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(self):
        self.variables: AbstractSet[Variable] = set()
        self.terminals: AbstractSet[Terminal] = set()
        self.start_symbol: Any[Variable, None] = None
        self.productions: Dict[Variable, Regex] = dict()

    @staticmethod
    def from_cfg(cfg: CFG) -> "ECFG":
        """
        Create ECFG from pyformlang CFG
        """
        return ECFG.from_text(cfg.to_text())

    @staticmethod
    def from_text(text: str) -> "ECFG":
        """
        Create ECFG from text
        """
        regexes = dict()
        bodies = set()
        terminals = set()
        for line in text.strip().split("\n"):
            var, body = map(str.strip, line.split("->"))
            if var in regexes:
                regexes[var] += " | " + body
            else:
                regexes[var] = body

            symbols = {s for s in body.split(" ") if s}
            symbols = {sym[:-1] if sym[-1] == "*" else sym for sym in symbols}
            terminals = terminals.union(
                {Terminal(sym) for sym in symbols if sym[0].islower()}
            )
            bodies.add(body)

        regexes = {var: Regex(body) for var, body in regexes.items()}
        ecfg = ECFG()
        ecfg.terminals = terminals
        ecfg.variables = {Variable(var) for var in regexes.keys()}
        ecfg.start_symbol = Variable("S")
        ecfg.productions = regexes
        return ecfg

    @staticmethod
    def from_file(file_name: str) -> "ECFG":
        """
        Create ECFG from file
        """
        with open(file_name) as file:
            return ECFG.from_text(file.read())
