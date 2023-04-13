from typing import Any, Dict, Tuple
from pyformlang.cfg import CFG, Variable
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol
from project.ecfg import ECFG
from scipy.sparse import csr_matrix

from project.finite_automata_utils import get_bool_matrices_for_fa


class RFA:
    def __init__(self):
        self.ecfg: Any[ECFG, None] = None
        self.fa_dict: Dict[Variable, EpsilonNFA] = dict()

    def minimize(self) -> "RFA":
        """
        Minimize finite automatons for every production
        Return minimized RFA
        """
        rfa = RFA()
        rfa.ecfg = self.ecfg
        rfa.fa_dict = {var: fa.minimize() for var, fa in self.fa_dict.items()}
        return rfa

    def to_matrices(
        self,
    ) -> Dict[Variable, Tuple[Dict[Symbol, csr_matrix], Dict[State, int]]]:
        """
        Get bool matrices of finite automatons for every production
        Return matrices for every symbol and indexes of every state
        """
        return {var: get_bool_matrices_for_fa(var) for var in self.fa_dict.keys()}

    @staticmethod
    def from_ecfg(ecfg: ECFG) -> "RFA":
        """
        Create RFA from ECFG
        """
        rfa = RFA()
        rfa.ecfg = ecfg
        rfa.fa_dict = {
            var: regex.to_epsilon_nfa() for var, regex in ecfg.productions.items()
        }
        return rfa

    @staticmethod
    def from_cfg(cfg: CFG) -> "RFA":
        """
        Create RFA from pyformlang CFG
        """
        return RFA.from_ecfg(ECFG.from_cfg(cfg))

    @staticmethod
    def from_text(text: str) -> "RFA":
        """
        Create RFA from text
        """
        return RFA.from_ecfg(ECFG.from_text(text))

    @staticmethod
    def from_file(file_name: str) -> "RFA":
        """
        Create RFA from file
        """
        return RFA.from_ecfg(ECFG.from_file(file_name))
