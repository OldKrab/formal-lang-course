import os
from project.rfa import RFA
from tests.ecfg.test_creation import default_cfg


def test_minimize():
    dfa = RFA.from_cfg(default_cfg())
    min_dfa = dfa.minimize()

    dfa_orig = RFA.from_cfg(default_cfg())
    for var, fa in dfa.fa_dict.items():
        assert dfa_orig.fa_dict[var] == fa

    for var, fa in dfa.fa_dict.items():
        min_fa = fa.minimize()
        assert min_dfa.fa_dict[var] == min_fa
