from networkx import MultiDiGraph
import pytest
from project.language.parser import check_syntax, to_dot
from antlr4.error.Errors import ParseCancellationException
from networkx.drawing import nx_agraph, nx_pydot


def test_print():
    text = "ВЫВЕСТИ 42"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [("program_1", "print_2", "0"), ("print_2", "int_val_3", "0")]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_bind():
    text = 'ПУСТЬ x = "str"'
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "bind_2", "0"),
            ("bind_2", "var_3", "0"),
            ("bind_2", "str_val_4", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_without_brackets():
    text = "ВЫВЕСТИ x ++ y ++ z"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "concat_expr_3", "0"),
            ("concat_expr_3", "concat_expr_4", "0"),
            ("concat_expr_4", "var_5", "0"),
            ("concat_expr_4", "var_6", "0"),
            ("concat_expr_3", "var_7", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_with_brackets():
    text = "ВЫВЕСТИ x И (y ИЛИ z)"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "intersect_expr_3", "0"),
            ("intersect_expr_3", "var_4", "0"),
            ("intersect_expr_3", "union_expr_5", "0"),
            ("union_expr_5", "var_6", "0"),
            ("union_expr_5", "var_7", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_exprs():
    text = 'ВЫВЕСТИ ({42*, "str"}, 1 == 1, 1 ИЛИ 1, 1 И 1, 1 ПРИНАДЛЕЖИТ 1, 1 ПОДМНОЖЕСТВО ДЛЯ 1, НЕ 1, {1..1})'
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "tuple_val_3", "0"),
            ("tuple_val_3", "set_val_4", "0"),
            ("set_val_4", "klein_expr_5", "0"),
            ("klein_expr_5", "int_val_6", "0"),
            ("set_val_4", "str_val_7", "0"),
            ("tuple_val_3", "equal_expr_8", "0"),
            ("equal_expr_8", "int_val_9", "0"),
            ("equal_expr_8", "int_val_10", "0"),
            ("tuple_val_3", "union_expr_11", "0"),
            ("union_expr_11", "int_val_12", "0"),
            ("union_expr_11", "int_val_13", "0"),
            ("tuple_val_3", "intersect_expr_14", "0"),
            ("intersect_expr_14", "int_val_15", "0"),
            ("intersect_expr_14", "int_val_16", "0"),
            ("tuple_val_3", "in_set_expr_17", "0"),
            ("in_set_expr_17", "int_val_18", "0"),
            ("in_set_expr_17", "int_val_19", "0"),
            ("tuple_val_3", "subset_expr_20", "0"),
            ("subset_expr_20", "int_val_21", "0"),
            ("subset_expr_20", "int_val_22", "0"),
            ("tuple_val_3", "not_expr_23", "0"),
            ("not_expr_23", "int_val_24", "0"),
            ("tuple_val_3", "set_val_25", "0"),
            ("set_val_25", "set_interval_26", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_lambda():
    text = "ВЫВЕСТИ x -> 1"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "lambda_expr_3", "0"),
            ("lambda_expr_3", "var_4", "0"),
            ("lambda_expr_3", "int_val_5", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.edges) == set(result_graph.edges)
    assert set(expected_graph.nodes) == set(result_graph.nodes)


def test_set():
    text = "ВЫВЕСТИ УСТАНОВИТЬ x КАК СТАРТОВЫЕ ДЛЯ УСТАНОВИТЬ x КАК ФИНАЛЬНЫЕ ДЛЯ x"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "set_start_expr_3", "0"),
            ("set_start_expr_3", "var_4", "0"),
            ("set_start_expr_3", "set_final_expr_5", "0"),
            ("set_final_expr_5", "var_6", "0"),
            ("set_final_expr_5", "var_7", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_add():
    text = "ВЫВЕСТИ ДОБАВИТЬ x К СТАРТОВЫМ ДЛЯ ДОБАВИТЬ x К ФИНАЛЬНЫМ ДЛЯ x"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "add_start_expr_3", "0"),
            ("add_start_expr_3", "var_4", "0"),
            ("add_start_expr_3", "add_final_expr_5", "0"),
            ("add_final_expr_5", "var_6", "0"),
            ("add_final_expr_5", "var_7", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_from():
    text = "ВЫВЕСТИ СТАРТОВЫЕ ИЗ ФИНАЛЬНЫЕ ИЗ ВЕРШИНЫ ИЗ РЕБРА ИЗ МЕТКИ ИЗ x"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "start_from_expr_3", "0"),
            ("start_from_expr_3", "final_from_expr_4", "0"),
            ("final_from_expr_4", "vertexes_from_expr_5", "0"),
            ("vertexes_from_expr_5", "edges_from_expr_6", "0"),
            ("edges_from_expr_6", "labels_from_expr_7", "0"),
            ("labels_from_expr_7", "var_8", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_load():
    text = "ВЫВЕСТИ ЗАГРУЗИТЬ x"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "load_expr_3", "0"),
            ("load_expr_3", "var_4", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)


def test_functors():
    text = "ВЫВЕСТИ ОТОБРАЗИТЬ x ФИЛЬТРОВАТЬ x x"
    test_file = "test.dot"
    expected_graph = MultiDiGraph(
        [
            ("program_1", "print_2", "0"),
            ("print_2", "map_expr_3", "0"),
            ("map_expr_3", "var_4", "0"),
            ("map_expr_3", "filter_expr_5", "0"),
            ("filter_expr_5", "var_6", "0"),
            ("filter_expr_5", "var_7", "0"),
        ]
    )
    to_dot(text, test_file)
    result_graph = nx_agraph.read_dot(test_file)
    assert set(expected_graph.nodes) == set(result_graph.nodes)
    assert set(expected_graph.edges) == set(result_graph.edges)
