import cfpq_data
import networkx as nx
import networkx.drawing.nx_pydot as nx_pydot
from typing import Any, Iterable, Set, NamedTuple, Tuple, Union
import pyformlang.finite_automaton as fa
import pyformlang.regular_expression as re


def _load_graph(name: str) -> nx.MultiDiGraph:
    path = cfpq_data.download(name)
    return cfpq_data.graph_from_csv(path)


def _get_graph_vertexes_number(gr: nx.MultiDiGraph) -> int:
    return gr.number_of_nodes()


def _get_graph_edges_number(gr: nx.MultiDiGraph) -> int:
    return gr.number_of_edges()


def _get_graph_unique_labels(gr: nx.MultiDiGraph) -> Set[str]:
    return {data["label"] for (_, _, data) in gr.edges(data=True)}


GraphInfo = NamedTuple(
    "GraphInfo",
    [("vertexes_count", int), ("edges_count", int), ("unique_labels", Set[str])],
)


def get_graph_info(name: str) -> GraphInfo:
    graph = _load_graph(name)
    return GraphInfo(
        vertexes_count=_get_graph_vertexes_number(graph),
        edges_count=_get_graph_edges_number(graph),
        unique_labels=_get_graph_unique_labels(graph),
    )


def save_labeled_two_cycles_graph(
    n: int, m: int, labels: Tuple[str, str], path: str
) -> None:
    gr = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    nx_pydot.write_dot(gr, path)


def build_min_dfa_from_regex(regex_str: str) -> fa.DeterministicFiniteAutomaton:
    return re.PythonRegex(regex_str).to_epsilon_nfa().minimize()


def convert_nx_graph_to_nfa(
    nx_graph: nx.MultiDiGraph,
    start_states: Union[Iterable[Any], None] = None,
    final_states: Union[Iterable[Any], None] = None,
) -> fa.NondeterministicFiniteAutomaton:
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
