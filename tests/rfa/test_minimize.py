import os
from project.rsm import RSM
from tests.ecfg.test_creation import default_cfg


def test_minimize():
    dfa = RSM.from_cfg(default_cfg())
    min_dfa = dfa.minimize()

    dfa_orig = RSM.from_cfg(default_cfg())
    for var, fa in dfa.fa_dict.items():
        assert dfa_orig.fa_dict[var] == fa

    for var, fa in dfa.fa_dict.items():
        min_fa = fa.minimize()
        assert min_dfa.fa_dict[var] == min_fa
