import pytest
# on import will print something from __init__ file
import project.graph_utils as graph_utils
import os


def setup_module(module):
    pass


def teardown_module(module):
    pass


def test_s():
    path = "test.txt"
    labels = ('boob', 'loop')
    n, m = 2, 3

    graph_utils.save_labeled_two_cycles_graph(n, m, labels, path)

    expected_gr = """digraph  {
1;
2;
0;
3;
4;
5;
1 -> 2  [key=0, label=boob];
2 -> 0  [key=0, label=boob];
0 -> 1  [key=0, label=boob];
0 -> 3  [key=0, label=loop];
3 -> 4  [key=0, label=loop];
4 -> 5  [key=0, label=loop];
5 -> 0  [key=0, label=loop];
}
"""
    with open(path) as file:
        actual_gr = file.read()
    os.remove(path)

    assert actual_gr == expected_gr
