from functools import reduce
from typing import Any, Iterable, Union, Dict, Tuple, Set
from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    State,
    Symbol,
)
from pyformlang.regular_expression import PythonRegex
import networkx as nx
from scipy.sparse import csr_matrix, kron
import numpy as np


def build_min_dfa_from_regex(regex_str: str) -> DeterministicFiniteAutomaton:
    """
    Build minimal DFA from python regex
    """
    return PythonRegex(regex_str).to_epsilon_nfa().minimize()


def convert_nx_graph_to_nfa(
    nx_graph: nx.MultiDiGraph,
    start_states: Union[Iterable[Any], None] = None,
    final_states: Union[Iterable[Any], None] = None,
) -> NondeterministicFiniteAutomaton:
    """
    Convert NetworkX MultiDiGraph to NFA.
    You can specify start and final states. By default, all states are start and final.
    """
    nfa = FiniteAutomaton.from_networkx(nx_graph).remove_epsilon_transitions()
    if start_states is None:
        start_states = nfa.states
    if final_states is None:
        final_states = nfa.states
    for start_state in start_states:
        nfa.add_start_state(start_state)
    for final_state in final_states:
        nfa.add_final_state(final_state)
    return nfa


def _get_bool_matrices_for_fa(
    fa: EpsilonNFA,
) -> Tuple[Dict[Symbol, csr_matrix], Dict[State, int]]:
    def get_bool_matrix(n):
        return csr_matrix((n, n), dtype=np.bool_)

    states_idxs = {s: i for i, s in enumerate(fa.states)}
    bool_matrices = {symb: get_bool_matrix(len(fa.states)) for symb in fa.symbols}
    for s_from, symbol, s_to in fa:
        matrix = bool_matrices[symbol]
        matrix[states_idxs[s_from], states_idxs[s_to]] = True
    return bool_matrices, states_idxs


def _intersect_matrices(lhs_fa, rhs_fa):
    lhs_matrices, _ = _get_bool_matrices_for_fa(lhs_fa)
    rhs_matrices, _ = _get_bool_matrices_for_fa(rhs_fa)
    symbols = lhs_fa.symbols.intersection(rhs_fa.symbols)
    matrices = {symb: kron(lhs_matrices[symb], rhs_matrices[symb]) for symb in symbols}

    def get_pairs_states(lhs_states, rhs_states):
        return [State((lhs_s, rhs_s)) for lhs_s in lhs_states for rhs_s in rhs_states]

    states = get_pairs_states(lhs_fa.states, rhs_fa.states)
    start_states = get_pairs_states(lhs_fa.start_states, rhs_fa.start_states)
    final_states = get_pairs_states(lhs_fa.final_states, rhs_fa.final_states)

    return matrices, states, start_states, final_states


def intersect_two_fa(lhs_fa: EpsilonNFA, rhs_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Intersect one EpsilonNFA with other.
    The result is EpsilonNFA that accepts only words that accept both original NFA's.
    The result states is pairs of states original NFA's.
    """
    matrices, states, start_states, final_states = _intersect_matrices(lhs_fa, rhs_fa)

    result_fa = EpsilonNFA()
    for symb, matrix in matrices.items():
        for row, col in zip(*matrix.nonzero()):
            s_from = states[row]
            s_to = states[col]
            result_fa.add_transition(s_from, symb, s_to)
            if s_from in start_states:
                result_fa.add_start_state(s_from)
            if s_to in final_states:
                result_fa.add_final_state(s_to)

    return result_fa


def query_regex_to_fa(db_fa: EpsilonNFA, query: str) -> Set[Tuple[State, State]]:
    """
    Execute query regex to finite automaton.
    Return all pairs of start and final states of fa that form word corresponding to the regex.
    """

    def get_transitive_closure(matrix: csr_matrix):
        prev_count = 0
        res: csr_matrix = matrix.copy()
        while res.count_nonzero() != prev_count:
            prev_count = res.count_nonzero()
            res = res + (res @ res)
        return res

    def union_matrix(matrix: Dict[Symbol, csr_matrix]):
        return reduce(lambda res, m: res + m, matrix.values())

    def get_db_pair(s_from, s_to):
        db_s_from, _ = s_from.value
        db_s_to, _ = s_to.value
        return (db_s_from, db_s_to)

    query_fa = build_min_dfa_from_regex(query)
    matrices, states, start_states, final_states = _intersect_matrices(db_fa, query_fa)
    closure = get_transitive_closure(union_matrix(matrices))
    result = set()
    for row, col in zip(*closure.nonzero()):
        s_from = states[row]
        s_to = states[col]
        if s_from in start_states and s_to in final_states:
            db_pair = get_db_pair(s_from, s_to)
            if not db_pair in result:
                result.add(db_pair)
    return result
