from typing import Any, Dict, Tuple
from pyformlang.cfg import CFG, Variable
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol
from project.ecfg import ECFG
from scipy.sparse import csr_matrix

from project.finite_automata_utils import (
    get_bool_matrices_for_fa,
    get_edges_of_fa,
    get_final_states_of_fa,
    get_labels_of_fa,
    get_start_states_of_fa,
    get_states_of_fa,
)


class RSM:
    def __init__(self):
        self.ecfg: Any[ECFG, None] = None
        self.fa_dict: Dict[Variable, EpsilonNFA] = dict()
        self.start_symbol: Variable = None

    def _get_start_fa(self):
        return self.fa_dict[self.start_symbol]

    def get_edges(self) -> set:
        """
        Return edges of start FA
        """
        return get_edges_of_fa(self._get_start_fa())

    def get_start_states(self) -> set:
        """
        Return start states of start FA
        """
        return get_start_states_of_fa(self._get_start_fa())

    def get_final_states(self) -> set:
        """
        Return final states of start FA
        """
        return get_final_states_of_fa(self._get_start_fa())

    def get_labels(self) -> set:
        """
        Return labels of start FA
        """
        return get_labels_of_fa(self._get_start_fa())

    def get_states(self) -> set:
        """
        Return vertexes of start FA
        """
        return get_states_of_fa(self._get_start_fa())

    def minimize(self) -> "RSM":
        """
        Minimize finite automatons for every production
        Return minimized RSM
        """
        rsm = RSM()
        rsm.ecfg = self.ecfg
        rsm.fa_dict = {var: fa.minimize() for var, fa in self.fa_dict.items()}
        return rsm

    def to_matrices(
        self,
    ) -> Dict[Variable, Tuple[Dict[Symbol, csr_matrix], Dict[State, int]]]:
        """
        Get bool matrices of finite automatons for every production
        Return matrices for every symbol and indexes of every state
        """
        return {var: get_bool_matrices_for_fa(var) for var in self.fa_dict.keys()}

    @staticmethod
    def from_ecfg(ecfg: ECFG) -> "RSM":
        """
        Create RSM from ECFG
        """
        rsm = RSM()
        rsm.start_symbol = ecfg.start_symbol
        rsm.ecfg = ecfg
        rsm.fa_dict = {
            var: regex.to_epsilon_nfa() for var, regex in ecfg.productions.items()
        }
        return rsm

    @staticmethod
    def from_cfg(cfg: CFG) -> "RSM":
        """
        Create RSM from pyformlang CFG
        """

        return RSM.from_ecfg(ECFG.from_cfg(cfg))

    @staticmethod
    def from_fa(fa: EpsilonNFA) -> "RSM":
        """
        Create RSM from pyformlang EpsilonNFA with one rule
        """
        rsm = RSM()
        rsm.start_symbol = Variable("S")
        rsm.fa_dict = {rsm.start_symbol: fa}
        return rsm

    @staticmethod
    def from_text(text: str) -> "RSM":
        """
        Create RSM from text
        """
        return RSM.from_ecfg(ECFG.from_text(text))

    @staticmethod
    def from_file(file_name: str) -> "RSM":
        """
        Create RSM from file
        """
        return RSM.from_ecfg(ECFG.from_file(file_name))
