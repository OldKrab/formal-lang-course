from typing import Any, Set, Tuple, Union
import numpy as np
from pyformlang.cfg import CFG, Terminal, Variable
import networkx as nx
from scipy.sparse import csr_matrix

from project.context_free_grammar import convert_cfg_to_wcnf, read_cfg_from_file


def _is_epsilon_body(body):
    return len(body) == 0


def _is_terminal_body(body, terminal=None):
    return len(body) == 1 and (terminal is None or Terminal(terminal) in body)


def _is_variable_body(body):
    return len(body) == 2


def _helling_all_result(
    graph: nx.MultiDiGraph, cfg: CFG
) -> Set[Tuple[Any, Variable, Any]]:
    def get_init_r():
        return {
            (v, prod.head, v)
            for v in graph.nodes
            for prod in cfg.productions
            if _is_epsilon_body(prod.body)
        } | {
            (v, prod.head, u)
            for v, u, t in graph.edges(data="label")
            for prod in cfg.productions
            if _is_terminal_body(prod.body, t)
        }

    r = get_init_r()
    queue = r.copy()
    while len(queue) > 0:
        v, N_i, u = queue.pop()
        r_diff = set()
        for v_2, N_j, u_2 in r:
            if u_2 == v:
                for prod in cfg.productions:
                    if prod.body == [N_j, N_i]:
                        queue.add((v_2, prod.head, u))
                        r_diff.add((v_2, prod.head, u))

        for v_2, N_j, u_2 in r:
            if v_2 == u:
                for prod in cfg.productions:
                    if prod.body == [N_i, N_j]:
                        queue.add((v, prod.head, u_2))
                        r_diff.add((v, prod.head, u_2))
        r = r | r_diff
    return r


def _prepare_graph_and_cfg(graph: Union[nx.MultiDiGraph, str], cfg: Union[CFG, str]):
    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)
    if isinstance(graph, str):
        graph: nx.MultiDiGraph = nx.nx_pydot.from_pydot(graph)
    return graph, convert_cfg_to_wcnf(cfg)


def _filter_cfpq_result(
    result: Set[Tuple[Any, Variable, Any]],
    start_nodes: Union[Set[Any], None] = None,
    final_nodes: Union[Set[Any], None] = None,
    variable: Union[Variable, None] = None,
) -> Set[Tuple[Any, Variable, Any]]:
    start_pred = final_pred = var_pred = lambda _: True
    if start_nodes is not None:
        start_pred = lambda node: node in start_nodes
    if final_nodes is not None:
        final_pred = lambda node: node in final_nodes
    if variable is not None:
        var_pred = lambda v: v == variable

    return {
        (v, N, u)
        for v, N, u in result
        if start_pred(v) and var_pred(N) and final_pred(u)
    }


def helling(
    graph: Union[nx.MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_nodes: Union[Set[Any], None] = None,
    final_nodes: Union[Set[Any], None] = None,
    variable: Union[Variable, None] = None,
) -> Set[Tuple[Any, Variable, Any]]:
    """
    Applies the Helling algorithm to a given CFG and graph to find all paths in the graph
    that correspond to a string generated by the CFG.

    Args:
        graph: The graph to traverse.
        cfg: The CFG. It can be a `CFG` object or a string path to a file containing the CFG.
        start_nodes: A set of start nodes in the graph. If not provided, all nodes are considered start nodes.
        final_nodes: A set of final nodes in the graph. If not provided, all nodes are considered final nodes.
        variable: The variable to use for generating strings. If not provided, all variables are used.

    Returns:
        A set of tuples representing paths in the graph that correspond to a string generated
        by the CFG. Each tuple has the form (v, N, u), where v and u are nodes in the graph, and
        N is a variable in the CFG.
    """
    graph, cfg = _prepare_graph_and_cfg(graph, cfg)
    result = _helling_all_result(graph, cfg)
    return _filter_cfpq_result(result, start_nodes, final_nodes, variable)


def _matrix_all_result(
    graph: nx.MultiDiGraph, cfg: CFG
) -> Set[Tuple[Any, Variable, Any]]:

    nodes_list = list(graph.nodes)
    nodes_idxs = {node: i for i, node in enumerate(nodes_list)}

    n = len(graph.nodes)
    edges = {(nodes_idxs[u], x, nodes_idxs[v]) for u, v, x in graph.edges(data="label")}
    prods = [(p.head, p.body) for p in cfg.productions]
    matrices = {v: csr_matrix((n, n), dtype=np.bool_) for v in cfg.variables}
    for i, x, j in edges:
        for var, body in prods:
            if _is_terminal_body(body, x):
                matrices[var][i, j] = True

    for i in range(n):
        for var, body in prods:
            if _is_epsilon_body(body):
                matrices[var][i, i] = True

    matrices_changed = True
    while matrices_changed:
        matrices_changed = False
        cnt_nonzero = sum(m.count_nonzero() for m in matrices.values())

        for var, body in prods:
            if _is_variable_body(body):
                matrices[var] += matrices[body[0]] @ matrices[body[1]]

        matrices_changed = cnt_nonzero != sum(
            m.count_nonzero() for m in matrices.values()
        )

    result = {
        (nodes_list[i], var, nodes_list[j])
        for var, m in matrices.items()
        for i, j in zip(*m.nonzero())
    }

    return result


def matrix(
    graph: Union[nx.MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_nodes: Union[Set[Any], None] = None,
    final_nodes: Union[Set[Any], None] = None,
    variable: Union[Variable, None] = None,
) -> Set[Tuple[Any, Variable, Any]]:
    graph, cfg = _prepare_graph_and_cfg(graph, cfg)
    result = _matrix_all_result(graph, cfg)
    return _filter_cfpq_result(result, start_nodes, final_nodes, variable)
