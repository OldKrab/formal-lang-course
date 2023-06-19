from functools import reduce
from typing import Any, Iterable, Union, Dict, Tuple, Set
from pyformlang.cfg import Epsilon
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
from scipy.sparse import csr_matrix, kron, block_diag
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


def get_edges_of_fa(fa: EpsilonNFA) -> set:
    """
    Return edges of FA
    """
    return {(frm.value, symb.value, to.value) for frm, symb, to in fa}


def get_states_of_fa(fa: EpsilonNFA) -> set:
    """
    Return states of FA
    """
    return {st.value for st in fa.states}


def get_start_states_of_fa(fa: EpsilonNFA) -> set:
    """
    Return start states of FA
    """
    return {st.value for st in fa.start_states}


def get_final_states_of_fa(fa: EpsilonNFA) -> set:
    """
    Return final states of FA
    """
    return {st.value for st in fa.final_states}


def get_labels_of_fa(fa: EpsilonNFA) -> set:
    """
    Return labels of FA
    """
    return {symb.value for frm, symb, to in fa}


def set_starts_of_fa(symbols: set, fa: EpsilonNFA):
    """
    Set starts symbols of FA
    """
    fa._start_state = set()
    for s in symbols:
        fa.add_start_state(s)


def set_finals_of_fa(symbols: set, fa: EpsilonNFA):
    """
    Set finals symbols of FA
    """
    fa._final_states = set()
    for s in symbols:
        fa.add_final_state(s)


def add_starts_to_fa(symbols: set, fa: EpsilonNFA):
    """
    Add starts symbols to FA
    """
    for s in symbols:
        fa.add_start_state(s)


def add_finals_to_fa(symbols: set, fa: EpsilonNFA):
    """
    Add finals symbols to FA
    """
    for s in symbols:
        fa.add_final_state(s)


def get_bool_matrices_for_fa(
    fa: EpsilonNFA,
) -> Tuple[Dict[Symbol, csr_matrix], Dict[State, int]]:
    """
    Get bool matrices for finite automaton
    Return matrices for every symbol and indexes of every state
    """

    def get_bool_matrix(n):
        return csr_matrix((n, n), dtype=np.bool_)

    states_idxs = {s: i for i, s in enumerate(fa.states)}
    bool_matrices = {symb: get_bool_matrix(len(fa.states)) for symb in fa.symbols}
    for s_from, symbol, s_to in fa:
        matrix = bool_matrices[symbol]
        matrix[states_idxs[s_from], states_idxs[s_to]] = True
    return bool_matrices, states_idxs


def _intersect_matrices(lhs_fa, rhs_fa):
    lhs_matrices, _ = get_bool_matrices_for_fa(lhs_fa)
    rhs_matrices, _ = get_bool_matrices_for_fa(rhs_fa)
    symbols = lhs_fa.symbols.intersection(rhs_fa.symbols)
    matrices = {symb: kron(lhs_matrices[symb], rhs_matrices[symb]) for symb in symbols}

    def get_pairs_states(lhs_states, rhs_states):
        return [
            State((lhs_s.value, rhs_s.value))
            for lhs_s in lhs_states
            for rhs_s in rhs_states
        ]

    states = get_pairs_states(lhs_fa.states, rhs_fa.states)
    start_states = get_pairs_states(lhs_fa.start_states, rhs_fa.start_states)
    final_states = get_pairs_states(lhs_fa.final_states, rhs_fa.final_states)

    return matrices, states, start_states, final_states


def union_of_two_fa(lhs_fa: EpsilonNFA, rhs_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Union one EpsilonNFA with the other.
    The result is EpsilonNFA that accepts words that accept one of original NFA's.
    """
    fa = EpsilonNFA()

    for fro, symb, to in lhs_fa:
        fa.add_transition(fro.value, symb, to.value)

    for fro, symb, to in rhs_fa:
        fa.add_transition(fro.value, symb, to.value)

    for node in lhs_fa.start_states:
        fa.add_start_state(node.value)

    for node in rhs_fa.start_states:
        fa.add_start_state(node.value)

    for node in lhs_fa.final_states:
        fa.add_final_state(node.value)

    for node in rhs_fa.final_states:
        fa.add_final_state(node.value)

    return fa


def concat_of_two_fa(lhs_fa: EpsilonNFA, rhs_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Concat one EpsilonNFA with the other.
    """
    fa = EpsilonNFA()

    for fro, symb, to in lhs_fa:
        fa.add_transition(fro.value, symb, to.value)

    for fro, symb, to in rhs_fa:
        fa.add_transition(fro.value, symb, to.value)

    for node in lhs_fa.start_states:
        fa.add_start_state(node.value)

        for node2 in rhs_fa.final_states:
            fa.add_transition(node.value, Epsilon(), node2.value)

    for node in rhs_fa.final_states:
        fa.add_final_state(node.value)

    return fa


def intersect_two_fa(lhs_fa: EpsilonNFA, rhs_fa: EpsilonNFA) -> EpsilonNFA:
    """
    Intersect one EpsilonNFA with the other.
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
        return db_s_from, db_s_to

    query_fa = build_min_dfa_from_regex(query)
    matrices, states, start_states, final_states = _intersect_matrices(db_fa, query_fa)
    closure = get_transitive_closure(union_matrix(matrices))
    result = set()
    for row, col in zip(*closure.nonzero()):
        s_from = states[row]
        s_to = states[col]
        if s_from in start_states and s_to in final_states:
            db_pair = get_db_pair(s_from, s_to)
            if db_pair not in result:
                result.add(db_pair)
    return result


def query_regex_to_fa_with_states(
    db_graph: nx.MultiDiGraph,
    query: str,
    start_states: Union[Iterable[Any], None] = None,
    final_states: Union[Iterable[Any], None] = None,
) -> Set[Tuple[State, State]]:
    """
    Execute query regex to finite automaton with given start and final states.
    Return all pairs of start and final states of fa that form word corresponding to the regex.
    """

    return query_regex_to_fa(
        convert_nx_graph_to_nfa(db_graph, start_states, final_states), query
    )


def find_reachable_in_fa_from_any(
    db_fa: EpsilonNFA, regex: str, db_start_states: Iterable[Any] = None
) -> Set[Any]:
    """
    Execute query regex to finite automaton.
    Return all reachable states from given db_start_states.
    """
    if db_start_states is None:
        db_start_states = db_fa.start_states
    query_fa = build_min_dfa_from_regex(regex)
    db_matrices, db_state_idx = get_bool_matrices_for_fa(db_fa)
    query_matrices, query_state_idx = get_bool_matrices_for_fa(query_fa)
    db_cnt = len(db_fa.states)
    query_cnt = len(query_fa.states)

    def init_front():
        front = csr_matrix((db_cnt + query_cnt, query_cnt), dtype=np.bool_)
        for db_s in db_start_states:
            for q_s in query_fa.start_states:
                i = db_state_idx[db_s]
                j = query_state_idx[q_s]
                front[i, j] = True
        for q_s in query_fa.start_states:
            j = query_state_idx[q_s]
            front[db_cnt + j, j] = True
        return front

    def step(front: csr_matrix, all_transitions: Iterable[csr_matrix]):
        new_front = csr_matrix((db_cnt + query_cnt, query_cnt), dtype=np.bool_)
        for transitions in all_transitions:
            prod_res = transitions @ front
            for i in range(query_cnt):
                for j in range(query_cnt):
                    if prod_res[db_cnt + i, j]:
                        new_front[:, i] += prod_res[:, j]
        return new_front

    symbols = db_fa.symbols.intersection(query_fa.symbols)
    all_transitions = [
        block_diag((db_matrices[symb], query_matrices[symb])).transpose()
        for symb in symbols
    ]

    front = init_front()
    reachable = front.copy()
    prev_count = 0
    while reachable.count_nonzero() != prev_count:
        prev_count = reachable.count_nonzero()
        front = step(front, all_transitions)
        reachable += front

    res = set()
    db_states = {i: s for s, i in db_state_idx.items()}
    for q_f in query_fa.final_states:
        j = query_state_idx[q_f]
        for i in range(db_cnt):
            if reachable[i, j]:
                res.add(db_states[i].value)
    return res


def find_reachable_in_fa_from_each(
    db_fa: EpsilonNFA, regex: str, db_start_states: Union[Iterable[Any], None]
) -> Dict[Any, Set[Any]]:
    """
    Execute query regex to finite automaton.
    Return dict of all reachable states from each of given db_start_states.
    """

    return {
        start: find_reachable_in_fa_from_any(db_fa, regex, [start])
        for start in db_start_states
    }


def find_reachable_in_graph_from_any(
    db_graph: nx.MultiDiGraph,
    regex: str,
    db_start_states: Iterable[Any],
    db_final_states: Iterable[Any],
) -> Set[Any]:
    """
    Execute query regex to graph.
    Return all reachable states from given db_start_states.
    """
    db_fa = convert_nx_graph_to_nfa(db_graph)
    states = find_reachable_in_fa_from_any(db_fa, regex, db_start_states)
    return states.intersection(set(db_final_states))


def find_reachable_in_graph_from_each(
    db_graph: nx.MultiDiGraph,
    regex: str,
    db_start_states: Iterable[Any],
    db_final_states: Iterable[Any],
) -> Dict[Any, Set[Any]]:
    """
    Execute query regex to graph.
    Return dict of all reachable states from each of given db_start_states.
    """
    db_fa = convert_nx_graph_to_nfa(db_graph)
    res = find_reachable_in_fa_from_each(db_fa, regex, db_start_states)
    final_set = set(db_final_states)
    return {start: states.intersection(final_set) for start, states in res.items()}
