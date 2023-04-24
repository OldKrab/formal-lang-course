from pyformlang.cfg import CFG


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
