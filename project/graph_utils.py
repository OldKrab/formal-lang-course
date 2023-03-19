from typing import Set, NamedTuple, Tuple
import cfpq_data
import networkx as nx
import networkx.drawing.nx_pydot as nx_pydot


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
    """Return tuple of vertex count, edges count and unique labels of graph from cfpq_data repository by name"""
    graph = _load_graph(name)
    return GraphInfo(
        vertexes_count=_get_graph_vertexes_number(graph),
        edges_count=_get_graph_edges_number(graph),
        unique_labels=_get_graph_unique_labels(graph),
    )


def save_labeled_two_cycles_graph(
    n: int, m: int, labels: Tuple[str, str], path: str
) -> None:
    """Create labeled two cycles graph with n and m vertexes and save it to path"""
    gr = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    nx_pydot.write_dot(gr, path)
