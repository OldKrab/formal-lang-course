import os
from networkx.drawing import nx_pydot
from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import PythonRegex
import pytest
from project.language.interpreter import interpret
from project.language.parser import check_syntax
from antlr4.error.Errors import ParseCancellationException
import networkx as nx


def assert_output(strings):
    for code, expected in strings:
        try:
            assert interpret(code).strip() == expected.strip()
        except Exception as ex:
            pytest.fail(f"Raise for code: {code}, ex: {ex}")


def assert_throw(strings):
    for code in strings:
        try:
            interpret(code)
        except Exception:
            continue
        pytest.fail(f"Not raise for code: {code}")


def write_regex(regex, file):
    nx_pydot.write_dot(
        PythonRegex(regex).to_epsilon_nfa().minimize().to_networkx(), file
    )


def write_graph(gr: EpsilonNFA, file):
    gr.write_as_dot(file)


def test_simple_print():
    assert_output(
        [
            ("ВЫВЕСТИ 42", "42"),
            ('ВЫВЕСТИ "42"', "42"),
            ("ВЫВЕСТИ {42, 24}", "{24, 42}"),
            ("ВЫВЕСТИ (42, 24)", "(42, 24)"),
        ]
    )

    assert_throw(['ВЫВЕСТИ КА ИЗ "x"' 'ВЫВЕСТИ РКА ИЗ КА ИЗ "x"'])


def test_load():
    file = "test.txt"
    write_regex("abc", file)
    code = f"""
    ПУСТЬ граф = ЗАГРУЗИТЬ "{file}"
    ВЫВЕСТИ {{"a", "b", "c"}} == МЕТКИ ИЗ граф
    """
    assert_output(
        [
            (code, "1"),
        ]
    )

    os.remove(file)


def test_str_to_fa():
    code = f"""
    ПУСТЬ рег = "abc"
    ВЫВЕСТИ {{"a", "b", "c"}} == МЕТКИ ИЗ КА ИЗ рег
    """
    assert_output(
        [
            (code, "1"),
        ]
    )


def test_fa_to_rsm():
    code = f"""
    ПУСТЬ рег = "abc"
    ВЫВЕСТИ {{"a", "b", "c"}} == МЕТКИ ИЗ РКА ИЗ КА ИЗ рег
    """
    assert_output(
        [
            (code, "1"),
        ]
    )


def test_set_add_starts_and_finals():
    file = "test.txt"
    gr = EpsilonNFA()
    gr.add_transitions([(1, "", 2), (2, "", 3), (3, "", 4)])
    write_graph(gr, file)
    code = f"""
    ПУСТЬ граф = ЗАГРУЗИТЬ "{file}"
    ПУСТЬ граф = УСТАНОВИТЬ {{"1"}} КАК СТАРТОВЫЕ ДЛЯ граф
    ПУСТЬ граф = УСТАНОВИТЬ {{"4"}} КАК ФИНАЛЬНЫЕ ДЛЯ граф
    ВЫВЕСТИ {{"1"}} == СТАРТОВЫЕ ИЗ граф
    ВЫВЕСТИ {{"4"}} == ФИНАЛЬНЫЕ ИЗ граф
    ПУСТЬ граф = ДОБАВИТЬ {{"2"}} К СТАРТОВЫМ ДЛЯ граф
    ПУСТЬ граф = ДОБАВИТЬ {{"3"}} К ФИНАЛЬНЫМ ДЛЯ граф
    ВЫВЕСТИ {{"1","2"}} == СТАРТОВЫЕ ИЗ граф
    ВЫВЕСТИ {{"3","4"}} == ФИНАЛЬНЫЕ ИЗ граф
    """
    assert_output(
        [
            (code, "1\n1\n1\n1"),
        ]
    )
    os.remove(file)


def test_any_from_graph():
    file = "test.txt"
    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "b", "3")])
    write_graph(gr, file)
    code = f"""
    ПУСТЬ граф = ЗАГРУЗИТЬ "{file}"
    ВЫВЕСТИ {{"1","2","3"}} == ВЕРШИНЫ ИЗ граф
    ВЫВЕСТИ {{("1", "a", "2"), ("2", "b", "3")}} == РЕБРА ИЗ граф
    ВЫВЕСТИ {{"a", "b"}} == МЕТКИ ИЗ граф
    """
    assert_output(
        [
            (code, "1\n1\n1"),
        ]
    )
    os.remove(file)


def test_reachable():
    file = "test.txt"
    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "b", "3")])
    write_graph(gr, file)
    code = f"""
    ПУСТЬ граф = УСТАНОВИТЬ {{"1"}} КАК СТАРТОВЫЕ ДЛЯ \
        УСТАНОВИТЬ {{"2", "3"}} КАК ФИНАЛЬНЫЕ ДЛЯ \
        ЗАГРУЗИТЬ "{file}"
    ВЫВЕСТИ ДОСТИЖИМЫЕ ИЗ граф С ОГРАНИЧЕНИЯМИ "a"
    ВЫВЕСТИ ДОСТИЖИМЫЕ ИЗ граф С ОГРАНИЧЕНИЯМИ "ab"

    """
    assert_output(
        [
            (code, "{2}\n{3}"),
        ]
    )
    os.remove(file)


def test_map_filter():

    code = f"""
    ПУСТЬ сет = {{1,2,3,4}}
    ПУСТЬ фильтр = ФИЛЬТРОВАТЬ (x -> НЕ (x == 1) И НЕ (x == 3)) сет
    ВЫВЕСТИ {{4,2}} == фильтр
    ВЫВЕСТИ {{"42","42"}} == ОТОБРАЗИТЬ (x -> "42") фильтр
    ВЫВЕСТИ {{}} == ФИЛЬТРОВАТЬ (x -> 0) сет
    """
    assert_output(
        [
            (code, "1\n1\n1"),
        ]
    )


def test_intersect():
    file, file2 = "test.txt", "test2.txt"
    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "b", "3")])
    write_graph(gr, file)

    gr = EpsilonNFA()
    gr.add_transitions([("1'", "a", "2'"), ("2'", "c", "3'")])
    write_graph(gr, file2)
    code = f"""
    ПУСТЬ ка1 = ЗАГРУЗИТЬ "{file}"
    ПУСТЬ ка2 = ЗАГРУЗИТЬ "{file2}"
    ПУСТЬ рез = ка1 И ка2
    ВЫВЕСТИ {{"a"}} == МЕТКИ ИЗ рез
    ВЫВЕСТИ {{("1", "1'"), ("2", "2'")}} == ВЕРШИНЫ ИЗ рез
    """
    assert_output(
        [
            (code, "1\n1"),
        ]
    )
    os.remove(file)
    os.remove(file2)


def test_union():
    file, file2 = "test.txt", "test2.txt"
    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "b", "3")])
    write_graph(gr, file)

    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "c", "4")])
    write_graph(gr, file2)
    code = f"""
    ПУСТЬ ка1 = ЗАГРУЗИТЬ "{file}"
    ПУСТЬ ка2 = ЗАГРУЗИТЬ "{file2}"
    ПУСТЬ рез = ка1 ИЛИ ка2
    ВЫВЕСТИ {{"a", "b", "c"}} == МЕТКИ ИЗ рез
    ВЫВЕСТИ {{"1", "2", "3", "4"}} == ВЕРШИНЫ ИЗ рез
    ПУСТЬ рез = УСТАНОВИТЬ {{"1"}} КАК СТАРТОВЫЕ ДЛЯ \
        УСТАНОВИТЬ {{"3", "4"}} КАК ФИНАЛЬНЫЕ ДЛЯ рез
    ВЫВЕСТИ {{"3", "4"}} == ДОСТИЖИМЫЕ ИЗ рез С ОГРАНИЧЕНИЯМИ ("ab" ИЛИ "ac")
    """
    assert_output(
        [
            (code, "1\n1\n1"),
        ]
    )
    os.remove(file)
    os.remove(file2)


def test_cancat():
    file, file2 = "test.txt", "test2.txt"
    gr = EpsilonNFA()
    gr.add_transitions([("1", "a", "2"), ("2", "b", "3")])
    write_graph(gr, file)

    gr = EpsilonNFA()
    gr.add_transitions([("4", "c", "5")])
    write_graph(gr, file2)
    code = f"""
    ПУСТЬ ка1 = УСТАНОВИТЬ {{"1"}} КАК СТАРТОВЫЕ ДЛЯ \
        УСТАНОВИТЬ {{"3"}} КАК ФИНАЛЬНЫЕ ДЛЯ ЗАГРУЗИТЬ "{file}"
    ПУСТЬ ка2 = УСТАНОВИТЬ {{"4"}} КАК СТАРТОВЫЕ ДЛЯ \
        УСТАНОВИТЬ {{"5"}} КАК ФИНАЛЬНЫЕ ДЛЯ ЗАГРУЗИТЬ "{file2}"
    ПУСТЬ рез = ка1 ++ ка2
    ВЫВЕСТИ {{"a", "b", "c"}} ПОДМНОЖЕСТВО ДЛЯ МЕТКИ ИЗ рез
    ВЫВЕСТИ {{"1", "2", "3", "4", "5"}} == ВЕРШИНЫ ИЗ рез
    """
    assert_output(
        [
            (code, "1\n1"),
        ]
    )
    os.remove(file)
    os.remove(file2)


def test_set_ops():
    code = f"""
    ПУСТЬ сет = {{1,2,3,4}}
    ВЫВЕСТИ {{1,2,4}} ПОДМНОЖЕСТВО ДЛЯ сет
    ВЫВЕСТИ НЕ ({{1,2,4,5}} ПОДМНОЖЕСТВО ДЛЯ сет)
    ВЫВЕСТИ 1 ПРИНАДЛЕЖИТ сет
    ВЫВЕСТИ НЕ (5 ПРИНАДЛЕЖИТ сет)
    """
    assert_output(
        [
            (code, "1\n1\n1\n1"),
        ]
    )
