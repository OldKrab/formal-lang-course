from dataclasses import dataclass
from typing import Any
from networkx.drawing import nx_pydot
from antlr4 import CommonTokenStream, InputStream, FileStream, StdinStream

from numpy import isin
from pyformlang.finite_automaton import EpsilonNFA, NondeterministicTransitionFunction
from pyformlang.regular_expression import PythonRegex
from project.finite_automata_utils import (
    add_finals_to_fa,
    add_starts_to_fa,
    build_min_dfa_from_regex,
    concat_of_two_fa,
    convert_nx_graph_to_nfa,
    find_reachable_in_fa_from_any,
    get_edges_of_fa,
    get_final_states_of_fa,
    get_labels_of_fa,
    get_start_states_of_fa,
    get_states_of_fa,
    intersect_two_fa,
    set_finals_of_fa,
    set_starts_of_fa,
    union_of_two_fa,
)
from project.language.antlr_generated.LanguageLexer import LanguageLexer
from project.language.antlr_generated.LanguageParser import LanguageParser
from project.language.antlr_generated.LanguageVisitor import LanguageVisitor
from project.language.parser import (
    check_syntax,
    get_parse_tree,
    get_parse_tree_from_file,
)
from project.rsm import RSM


def _interpret(tree_creator):
    vis = _InterpreterVisitor()
    tree = tree_creator()
    tree.accept(vis)
    return vis.output


def interpret(code: str):
    """
    Interprets the given code string and returns the output as a string.
    """
    return _interpret(lambda: get_parse_tree(code))


def interpret_file(file: str):
    """
    Interprets the code in the specified file and returns the output as a string.
    """
    return _interpret(lambda: get_parse_tree_from_file(file))


@dataclass
class _SetInterval:
    values: set


class _InterpreterVisitor(LanguageVisitor):
    def __init__(self):
        self._stack = []
        self._enter_scope()
        self.output = ""

    def _enter_scope(self):
        self._stack.append({})

    def _remove_scope(self):
        self._stack.pop()

    def _cur_frame(self):
        return self._stack[-1]

    def _add_id(self, id, value):
        self._cur_frame()[id] = value

    def _get_id_value(self, id):
        for frame in reversed(self._stack):
            if id in frame:
                return frame[id]

        raise Exception(f"Undefined variable {id}")

    def _raise_wrong_type(self):
        raise Exception("Unexpected type")

    def _print(self, s: str):
        self.output += s

    def _print_values_with_comma(self, values):
        first = True
        for val in values:
            if not first:
                self._print(", ")
            self._print_val(val)
            first = False

    def _print_tuple(self, tuple: tuple):
        self._print("(")
        self._print_values_with_comma(tuple)
        self._print(")")

    def _print_set(self, set: set):
        self._print("{")
        self._print_values_with_comma(set)
        self._print("}")

    def _print_val(self, value):
        if isinstance(value, str) or isinstance(value, int):
            self._print(str(value))
        elif isinstance(value, set):
            self._print_set(value)
        elif isinstance(value, tuple):
            self._print_tuple(value)
        else:
            self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#bind.
    def visitBind(self, ctx: LanguageParser.BindContext):
        id = ctx.var_decl().accept(self)
        expr = ctx.expr().accept(self)
        self._add_id(id, expr)

    # Visit a parse tree produced by LanguageParser#print.
    def visitPrint(self, ctx: LanguageParser.PrintContext):
        expr = ctx.expr().accept(self)
        self._print_val(expr)
        self._print("\n")

    # Visit a parse tree produced by LanguageParser#var_decl.
    def visitVar_decl(self, ctx: LanguageParser.Var_declContext):
        return ctx.ID().getText()

    # Visit a parse tree produced by LanguageParser#edges_from_expr.
    def visitEdges_from_expr(self, ctx: LanguageParser.Edges_from_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, RSM):
            res = expr.get_edges()
        elif isinstance(expr, EpsilonNFA):
            res = get_edges_of_fa(expr)
        else:
            self._raise_wrong_type()

        return res

    # Visit a parse tree produced by LanguageParser#not_expr.
    def visitNot_expr(self, ctx: LanguageParser.Not_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, int):
            return int(not expr)
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#fa_expr.
    def visitFa_expr(self, ctx: LanguageParser.Fa_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, str):
            return build_min_dfa_from_regex(expr)
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#rsm_expr.
    def visitRsm_expr(self, ctx: LanguageParser.Rsm_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, EpsilonNFA):
            return RSM.from_fa(expr)
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#vertexes_from_expr.
    def visitVertexes_from_expr(self, ctx: LanguageParser.Vertexes_from_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, RSM):
            res = expr.get_states()
        elif isinstance(expr, EpsilonNFA):
            res = get_states_of_fa(expr)
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#labels_from_expr.
    def visitLabels_from_expr(self, ctx: LanguageParser.Labels_from_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, RSM):
            res = expr.get_labels()
        elif isinstance(expr, EpsilonNFA):
            res = get_labels_of_fa(expr)
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#final_from_expr.
    def visitFinal_from_expr(self, ctx: LanguageParser.Final_from_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, RSM):
            res = expr.get_final_states()
        elif isinstance(expr, EpsilonNFA):
            res = get_final_states_of_fa(expr)
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#start_from_expr.
    def visitStart_from_expr(self, ctx: LanguageParser.Start_from_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, RSM):
            res = expr.get_start_states()
        elif isinstance(expr, EpsilonNFA):
            res = get_start_states_of_fa(expr)
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#reach_from_expr.
    def visitReach_from_expr(self, ctx: LanguageParser.Reach_from_exprContext):
        from_ = ctx.from_.accept(self)
        regex = ctx.limit.accept(self)
        if not (isinstance(from_, EpsilonNFA) and isinstance(regex, str)):
            self._raise_wrong_type()
        return find_reachable_in_fa_from_any(from_, regex)

    # Visit a parse tree produced by LanguageParser#concat_expr.
    def visitConcat_expr(self, ctx: LanguageParser.Concat_exprContext):
        lhs = ctx.expr(0).accept(self)
        rhs = ctx.expr(1).accept(self)
        if isinstance(lhs, EpsilonNFA) and isinstance(rhs, EpsilonNFA):
            res = concat_of_two_fa(lhs, rhs)
        elif isinstance(lhs, str) and isinstance(rhs, str):
            res = lhs + rhs
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#union_expr.
    def visitUnion_expr(self, ctx: LanguageParser.Union_exprContext):
        lhs = ctx.expr(0).accept(self)
        rhs = ctx.expr(1).accept(self)
        if isinstance(lhs, EpsilonNFA) and isinstance(rhs, EpsilonNFA):
            res = union_of_two_fa(lhs, rhs)
        elif isinstance(lhs, str) and isinstance(rhs, str):
            res = f"({lhs})|({rhs})"
        elif isinstance(lhs, int) and isinstance(rhs, int):
            res = lhs or rhs
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#intersect_expr.
    def visitIntersect_expr(self, ctx: LanguageParser.Intersect_exprContext):
        lhs = ctx.expr(0).accept(self)
        rhs = ctx.expr(1).accept(self)
        if isinstance(lhs, EpsilonNFA) and isinstance(rhs, EpsilonNFA):
            res = intersect_two_fa(lhs, rhs)
        elif isinstance(lhs, int) and isinstance(rhs, int):
            res = lhs and rhs
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#klein_expr.
    def visitKlein_expr(self, ctx: LanguageParser.Klein_exprContext):
        expr = ctx.expr().accept(self)
        if isinstance(expr, EpsilonNFA):
            res = expr.kleene_star()
        elif isinstance(expr, str):
            res = str(PythonRegex(expr).kleene_star())
        else:
            self._raise_wrong_type()
        return res

    # Visit a parse tree produced by LanguageParser#load_expr.
    def visitLoad_expr(self, ctx: LanguageParser.Load_exprContext):
        expr = ctx.expr().accept(self)
        if not isinstance(expr, str):
            self._raise_wrong_type()
        graph = nx_pydot.read_dot(expr)
        return convert_nx_graph_to_nfa(graph)

    # Visit a parse tree produced by LanguageParser#set_final_expr.
    def visitSet_final_expr(self, ctx: LanguageParser.Set_final_exprContext):
        symbols = ctx.what.accept(self)
        expr = ctx.for_.accept(self)
        if isinstance(expr, EpsilonNFA):
            set_finals_of_fa(symbols, expr)
        else:
            self._raise_wrong_type()
        return expr

    # Visit a parse tree produced by LanguageParser#set_start_expr.
    def visitSet_start_expr(self, ctx: LanguageParser.Set_start_exprContext):
        symbols = ctx.what.accept(self)
        expr = ctx.for_.accept(self)
        if isinstance(expr, EpsilonNFA):
            set_starts_of_fa(symbols, expr)
        else:
            self._raise_wrong_type()
        return expr

    # Visit a parse tree produced by LanguageParser#equal_expr.
    def visitEqual_expr(self, ctx: LanguageParser.Equal_exprContext):
        lhs = ctx.expr(0).accept(self)
        rhs = ctx.expr(1).accept(self)
        if (
            isinstance(lhs, int)
            and isinstance(rhs, int)
            or isinstance(lhs, set)
            and isinstance(rhs, set)
            or isinstance(lhs, tuple)
            and isinstance(rhs, tuple)
            or isinstance(lhs, str)
            and isinstance(rhs, str)
        ):
            return int(lhs == rhs)
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#in_set_expr.
    def visitIn_set_expr(self, ctx: LanguageParser.In_set_exprContext):
        what = ctx.what.accept(self)
        to = ctx.to.accept(self)
        if isinstance(to, set):
            return int(what in to)
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#subset_expr.
    def visitSubset_expr(self, ctx: LanguageParser.Subset_exprContext):
        what = ctx.what.accept(self)
        of = ctx.of.accept(self)
        if isinstance(what, set) and isinstance(of, set):
            return int(what.issubset(of))
        self._raise_wrong_type()

    # Visit a parse tree produced by LanguageParser#map_expr.
    def visitMap_expr(self, ctx: LanguageParser.Map_exprContext):
        s = ctx.what.accept(self)
        func = ctx.with_.accept(self)
        if not (isinstance(s, set) and callable(func)):
            self._raise_wrong_type()

        return set(map(func, s))

    # Visit a parse tree produced by LanguageParser#filter_expr.
    def visitFilter_expr(self, ctx: LanguageParser.Filter_exprContext):
        s = ctx.what.accept(self)
        func = ctx.with_.accept(self)
        b = func is callable
        if not (isinstance(s, set) and callable(func)):
            self._raise_wrong_type()

        return set(filter(func, s))

    # Visit a parse tree produced by LanguageParser#add_start_expr.
    def visitAdd_start_expr(self, ctx: LanguageParser.Add_start_exprContext):
        symbols = ctx.what.accept(self)
        expr = ctx.for_.accept(self)
        if isinstance(expr, EpsilonNFA) and isinstance(symbols, set):
            add_starts_to_fa(symbols, expr)
        else:
            self._raise_wrong_type()
        return expr

    # Visit a parse tree produced by LanguageParser#add_final_expr.
    def visitAdd_final_expr(self, ctx: LanguageParser.Add_final_exprContext):
        symbols = ctx.what.accept(self)
        expr = ctx.for_.accept(self)
        if isinstance(expr, EpsilonNFA) and isinstance(symbols, set):
            add_finals_to_fa(symbols, expr)
        else:
            self._raise_wrong_type()
        return expr

    # Visit a parse tree produced by LanguageParser#lambda.
    def visitLambda(self, ctx: LanguageParser.LambdaContext):
        var = ctx.var_decl().accept(self)
        expr = ctx.expr()

        def func(v):
            self._enter_scope()
            self._add_id(var, v)
            res = expr.accept(self)
            self._remove_scope()
            return res

        return func

    # Visit a parse tree produced by LanguageParser#var.
    def visitVar(self, ctx: LanguageParser.VarContext):
        return self._get_id_value(ctx.ID().getText())

    # Visit a parse tree produced by LanguageParser#int_val.
    def visitInt_val(self, ctx: LanguageParser.Int_valContext):
        return int(ctx.getText())

    # Visit a parse tree produced by LanguageParser#str_val.
    def visitStr_val(self, ctx: LanguageParser.Str_valContext):
        return ctx.getText()[1:-1]

    # Visit a parse tree produced by LanguageParser#tuple_val.
    def visitTuple_val(self, ctx: LanguageParser.Tuple_valContext):
        return tuple(expr.accept(self) for expr in ctx.expr())

    # Visit a parse tree produced by LanguageParser#set_val.
    def visitSet_val(self, ctx: LanguageParser.Set_valContext):
        res = set()
        for elem in ctx.set_elem():
            if isinstance(elem, _SetInterval):
                res.union(elem.values)
            else:
                res.add(elem.accept(self))
        return res

    # Visit a parse tree produced by LanguageParser#set_elem_interval.
    def visitSet_elem_interval(self, ctx: LanguageParser.Set_elem_intervalContext):
        return _SetInterval(set(range(ctx.from_, ctx.to)))

    # Visit a parse tree produced by LanguageParser#brackets_expr.
    def visitBrackets_expr(self, ctx: LanguageParser.Brackets_exprContext):
        return ctx.expr().accept(self)
