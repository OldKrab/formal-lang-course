import pytest
import project.graph_utils as graph_utils  # on import will print something from __init__ file


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_ls():
    expected = (1687, 1453, {"d", "a"})
    actual = graph_utils.get_graph_info("ls")
    assert expected == actual


def test_gzip():
    expected = (2687, 2293, {"a", "d"})
    actual = graph_utils.get_graph_info("gzip")
    assert expected == actual
