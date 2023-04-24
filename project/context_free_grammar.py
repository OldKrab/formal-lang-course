from typing import Any, Callable, List, Set, Tuple, Union
from pyformlang.cfg import CFG, Epsilon, Terminal, Variable
import networkx as nx


def convert_cfg_to_wcnf(cfg: CFG) -> CFG:
    """
    Convert context free grammar to weak Chomsky normal form.
    1. remove unit productions
    2. remove useless symbols
    3. remove productions with more than one terminal
    4. decompose productions with more than 2 symbols in rhs
    """
    new_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_productions = new_cfg._get_productions_with_only_single_terminals()
    new_productions = new_cfg._decompose_productions(new_productions)
    new_cfg = CFG(start_symbol=cfg.start_symbol, productions=set(new_productions))
    return new_cfg


def read_cfg_from_file(filename: str) -> CFG:
    """
    Read grammar from a file and return a CFG object.
    """
    with open(filename, "r") as file:
        grammar_text = file.read()
    cfg = CFG.from_text(grammar_text)
    return cfg


def get_wcnf_from_file(filename: str) -> CFG:
    """
    Read grammar from a file, convert it to WCNF and return a CFG object.
    """
    return convert_cfg_to_wcnf(read_cfg_from_file(filename))


def helling_algorithm_for_wcnf(
    graph: nx.MultiDiGraph, cfg: CFG
) -> Set[Tuple[Any, Variable, Any]]:
    """
    This function finds all paths in a graph that satisfy a given context-free grammar, using the Helling algorithm.
    The graph should be a networkx.MultiDiGraph and the cfg should be an instance of the CFG class.
    The output is a set of tuples, where each tuple represents a path that satisfies the grammar.
    """

    def is_epsilon_prod(prod):
        return len(prod.body) == 0

    def is_terminal_prod(prod, terminal):
        return len(prod.body) == 1 and terminal in prod.body

    def get_init_r():
        return {
            (v, prod.head, v)
            for v in graph.nodes
            for prod in cfg.productions
            if is_epsilon_prod(prod)
        } | {
            (v, prod.head, u)
            for v, u, t in graph.edges(data="label")
            for prod in cfg.productions
            if is_terminal_prod(prod, Terminal(t))
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


def helling_algorithm_for_cfg(graph: Union[nx.MultiDiGraph, str], cfg: Union[CFG, str]):
    """
    This function finds all paths in a graph that satisfy a given context-free grammar, using the Helling algorithm.
    graph can be either a networkx.MultiDiGraph or a string representing the path to a Graphviz file.
    cfg can be either a CFG instance or a string representing the path to a file containing a context-free grammar.
    The function returns a set of tuples, where each tuple represents a path that satisfies the grammar."""
    if isinstance(cfg, str):
        cfg = read_cfg_from_file(cfg)
    if isinstance(graph, str):
        graph: nx.MultiDiGraph = nx.nx_pydot.from_pydot(graph)
    return helling_algorithm_for_wcnf(graph, convert_cfg_to_wcnf(cfg))


def helling_algorithm(
    graph: Union[nx.MultiDiGraph, str],
    cfg: Union[CFG, str],
    start_nodes: Set[Any],
    final_nodes: Set[Any],
    variable: Variable,
):
    """
    This function finds all paths in a graph that satisfy a given context-free grammar, using the Helling algorithm.
    graph can be either a networkx MultiDiGraph or a string representing the path to a Graphviz file,
    cfg can be either a CFG instance or a string representing the path to a file containing a context-free grammar.
    The start_nodes and final_nodes arguments should be sets of nodes in the graph representing the starting and final states.
    The variable argument should be a non-terminal symbol from the context-free grammar that is used to filter the paths.

    The function returns a set of tuples, where each tuple represents a path that satisfies the grammar
        and starts from a start node, ends at a final node, and contains the non-terminal symbol `variable`.
    """
    result = helling_algorithm_for_cfg(graph, cfg)
    return {
        (v, N, u)
        for v, N, u in result
        if v in start_nodes and N == variable and u in final_nodes
    }
