import pytest
from project.language.parser import check_syntax
from antlr4.error.Errors import ParseCancellationException


def assert_complete(strings):
    for string in strings:
        try:
            check_syntax(string)
        except ParseCancellationException as ex:
            pytest.fail(f"Raise for string: {string}, ex: {ex}")


def assert_throw(strings):
    for string in strings:
        try:
            check_syntax(string)
        except ParseCancellationException:
            continue
        pytest.fail(f"Not raise for string: {string}")


def test_load():
    assert_complete(
        [
            'ПУСТЬ x = ЗАГРУЗИТЬ "hello"',
            'ПУСТЬ x = ЗАГРУЗИТЬ ""',
            "ПУСТЬ x = ЗАГРУЗИТЬ b",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = ЗАГРУЗИТЬ",
            'ПУСТЬ x = ЗАГРУЗИТЬ ИЗ "a"',
        ]
    )


def test_fa_and_rsm():
    assert_complete(
        [
            'ПУСТЬ x = КА ИЗ "hello"',
            "ПУСТЬ y = РКА ИЗ x",
        ]
    )


def test_bind():
    assert_complete(
        [
            "ПУСТЬ x = 5",
            'ПУСТЬ x = УСТАНОВИТЬ г КАК СТАРТОВЫЕ ДЛЯ (ЗАГРУЗИТЬ "test")',
            "ПУСТЬ x = (1, (2, 3))",
            'ПУСТЬ x = {1, "str", (2, 3)}',
            'ПУСТЬ x = "hello"',
        ]
    )
    assert_throw(
        [
            "a = 1",
            "ПУСТЬ x =",
            "ПУСТЬ x = ВЫВЕСТИ y",
            "ПУСТЬ x = y = 1",
            'x = "hello"',
            'ПУСТЬ x ЭТО "hello"',
            'ПУСТЬ x "hello"',
        ]
    )


def test_comments():
    assert_complete(
        [
            "// This is a comment",
            "// This is a long comment\n\n\n// And this is the rest of the comment",
            "/* This is a block comment */",
            "/*\nThis is a\nlong block comment\n*/",
        ]
    )
    assert_throw(["/* This block comment is not closed"])


def test_whitespace():
    assert_complete(
        [
            "ПУСТЬ x=1",
            "ПУСТЬ x = 1",
            "ПУСТЬ x=1\nПУСТЬ y=2",
            "ПУСТЬ x = 1\n\n\nПУСТЬ y = 2",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = 2\t ПУСТЬ x = 2",
        ]
    )


def test_print():
    assert_complete(
        ["ВЫВЕСТИ x", 'ВЫВЕСТИ "hello"', "ВЫВЕСТИ (1, 2, 3)", "ВЫВЕСТИ {1, 2, 3}"]
    )
    assert_throw(
        [
            "ВЫВЕСТИ",
            "ВЫВЕСТИ ВЫВЕСТИ x",
            "ВЫВЕСТИ x y",
            "ВЫВЕСТИ &",
            "ВЫВЕСТИ 'hello\"",
            "ВЫВЕСТИ ПУСТЬ x = 5",
            "ВЫВЕСТИ func()",
        ]
    )


def test_lambda_expr():
    assert_complete(
        [
            "ПУСТЬ f = (x) -> x И x",
            "ПУСТЬ f = y -> z -> y == z",
            "ПУСТЬ f = (x, y, z) -> {(x, y), z}",
            "ПУСТЬ f = h -> (d, e) -> (h, d, e)",
            "ПУСТЬ f = (a, b) -> (a ++ b, a ИЛИ b)",
            "ПУСТЬ f = y, x, z -> y == z",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ f = y x z -> y == z",
            "ПУСТЬ f = -> x",
        ]
    )


def test_brackets():
    assert_complete(
        [
            "ПУСТЬ x = (1)",
            "ПУСТЬ x = (x ++ 3)*",
            "ПУСТЬ x = ((x++y) И (((y))))",
        ]
    )
    assert_throw(["ПУСТЬ x = ()", "ПУСТЬ x = )x(", "ПУСТЬ x = (x"])


def test_set_expr():
    assert_complete(
        [
            "ПУСТЬ x = УСТАНОВИТЬ (ВЕРШИНЫ ИЗ г) КАК СТАРТОВЫЕ ДЛЯ g",
            "ПУСТЬ x = УСТАНОВИТЬ (1,2,3) КАК ФИНАЛЬНЫЕ ДЛЯ (УСТАНОВИТЬ {0, 100, 256} КАК СТАРТОВЫЕ ДЛЯ g)",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = УСТАНОВИТЬ ВЕРШИНЫ ИЗ г",
            'ПУСТЬ x = УСТАНОВИТЬ КАК СТАРТОВЫЕ ДЛЯ "Вершины"',
            "ПУСТЬ x = УСТАНОВИТЬ () КАК СТАРТОВЫЕ ДЛЯ г",
        ]
    )


def test_add_expr():
    assert_complete(
        [
            "ПУСТЬ x = ДОБАВИТЬ {1,2} К СТАРТОВЫМ ДЛЯ г1",
            "ПУСТЬ x = ДОБАВИТЬ 3 К ФИНАЛЬНЫМ ДЛЯ г2",
            "ПУСТЬ x = ДОБАВИТЬ {1,2} К СТАРТОВЫМ ДЛЯ ДОБАВИТЬ 3 К ФИНАЛЬНЫМ ДЛЯ г2",
            "ПУСТЬ x = ДОБАВИТЬ {1, 2} К ФИНАЛЬНЫМ ДЛЯ ((1, 2), 3)",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = ДОБАВИТЬ 1 К СТАРТОВЫМ ДЛЯ ",
            "ПУСТЬ x = ДОБАВИТЬ К СТАРТОВЫМ 1  ДЛЯ г",
            "ПУСТЬ x = ДОБАВИТЬ ДЛЯ г 1 К СТАРТОВЫМ ",
            "ПУСТЬ x = ДОБАВИТЬ 1 и 2 К СТАРТОВЫМ ДЛЯ г",
            "ПУСТЬ x = ДОБАВИТЬ 1 К СТАРТОВЫХ ДЛЯ г",
        ]
    )


def test_from_expr():
    assert_complete(
        [
            "ПУСТЬ x = СТАРТОВЫЕ ИЗ г",
            "ПУСТЬ x = ФИНАЛЬНЫЕ ИЗ (1, 2, 3)",
            'ПУСТЬ x = ВЕРШИНЫ ИЗ ЗАГРУЗИТЬ "graph.dot"',
            'ПУСТЬ x = РЕБРА ИЗ ЗАГРУЗИТЬ "graph.dot"',
            'ПУСТЬ x = МЕТКИ ИЗ (1, 2, "three")',
            "ПУСТЬ x = ДОСТИЖИМЫЕ ИЗ (1, (2, 3), (4, (5, 6)))",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = ИЗ г",
            "ПУСТЬ x = СТАРТОВЫЕ ИЗ",
            "ПУСТЬ x = ДОСТИЖИМЫЕ ИЗ 1, 2, 3",
            "ПУСТЬ x = ЭЛЕМЕНТ ИЗ ({1, 2, 3}, 4, 5)",
        ]
    )


def test_operations():
    assert_complete(
        [
            "ПУСТЬ x = 1 ++ 2",
            "ПУСТЬ x = (1, 2, 3) И (4, 5)",
            "ПУСТЬ x = (1, 2, 3) И (4, 5) ИЛИ 42",
            "ПУСТЬ x = {1, 2, 3} ИЛИ {3, 4, 5}",
            "ПУСТЬ x = {1, 2, 3} ИЛИ {3, 4, 5} ИЛИ 42",
            "ПУСТЬ x = {1, 2, 3}*",
            "ПУСТЬ x = 42**",
            "ПУСТЬ x = expr1 == expr2",
            "ПУСТЬ x = 1 ПРИНАДЛЕЖИТ {1, 2, 3}",
            "ПУСТЬ x = {1} ПОДМНОЖЕСТВО ДЛЯ {1, 2, 3}",
            "ПУСТЬ x = НЕ (x == y)",
            "ПУСТЬ x = НЕ НЕ (x == y)",
            "ПУСТЬ x = (x != y)",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = 1 ++ ",
            "ПУСТЬ x = 1 ИЛИ И",
            "ПУСТЬ x = x * 2",
            "ПУСТЬ x = 1 ПРИНАДЛЕЖИТ ПРИНАДЛЕЖИТ",
            "ПУСТЬ x = ПОДМНОЖЕСТВО {1, 2, 3}",
            'ПУСТЬ x = {1} ПОДМНОЖЕСТВО "set"',
            "ПУСТЬ x = НЕ НЕ == y",
        ]
    )


def test_tuple_val():
    assert_complete(
        [
            "ПУСТЬ x = (1, 2, 3)",
            'ПУСТЬ x = ("a", "b")',
            "ПУСТЬ x = (t1, {t2, 1, 2})",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = ()",
            "ПУСТЬ x = 1, 2, 3",
            'ПУСТЬ x = (1, "a",)',
            "ПУСТЬ x = (1 2 3)",
        ]
    )


def test_set_val_expr():
    assert_complete(
        [
            "ПУСТЬ x = {1, 2, 3}",
            "ПУСТЬ x = {(1, 2), (3, 4), (5, 6)}",
            "ПУСТЬ x = {(2, 3), {4, 5}, {6, 7}}",
            "ПУСТЬ x = {1..5}",
            "ПУСТЬ x = {1, 2, 3, 5..9}",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ x = {1, 2, 3" "ПУСТЬ x = {1, 2, 3,}",
            "ПУСТЬ x = {}}",
            "ПУСТЬ x = {{}",
            "ПУСТЬ x = {{1, 2}, {}}",
            "ПУСТЬ x = {2..5..2}",
            "ПУСТЬ x = {5..}",
        ]
    )


def test_var_names():
    assert_complete(
        [
            "ПУСТЬ x = 42",
            "ПУСТЬ _x = 42",
            "ПУСТЬ _ = 42",
            "ПУСТЬ x42 = 42",
            "ПУСТЬ x_42_ = 42",
            "ПУСТЬ x' = 42",
            "ПУСТЬ x = 42",
            "ПУСТЬ ПРИВЕТ = 42",
            "ПУСТЬ привет42 = 42",
        ]
    )
    assert_throw(
        [
            "ПУСТЬ 1 = 42",
            "ПУСТЬ 'x = 42",
            "ПУСТЬ 1x = 42",
        ]
    )
