from typing import Any, Iterable, Union
import pyformlang.finite_automaton as fa
import pyformlang.regular_expression as re
import networkx as nx


def build_min_dfa_from_regex(regex_str: str) -> fa.DeterministicFiniteAutomaton:
    """
    Build minimal DFA from python regex
    """
    return re.PythonRegex(regex_str).to_epsilon_nfa().minimize()


def convert_nx_graph_to_nfa(
    nx_graph: nx.MultiDiGraph,
    start_states: Union[Iterable[Any], None] = None,
    final_states: Union[Iterable[Any], None] = None,
) -> fa.NondeterministicFiniteAutomaton:
    """
    Convert NetworkX MultiDiGraph to NFA.
    You can specify start and final states. By default, all states are start and final.
    """
    nfa = fa.FiniteAutomaton.from_networkx(nx_graph).remove_epsilon_transitions()
    if start_states is None:
        start_states = nfa.states
    if final_states is None:
        final_states = nfa.states
    for start_state in start_states:
        nfa.add_start_state(start_state)
    for final_state in final_states:
        nfa.add_final_state(final_state)
    return nfa
