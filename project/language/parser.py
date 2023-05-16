from typing import Union
from antlr4 import CommonTokenStream, InputStream, FileStream, StdinStream
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from networkx import MultiDiGraph
from networkx.drawing import nx_agraph
from project.language.antlr_generated.LanguageLexer import LanguageLexer
from project.language.antlr_generated.LanguageParser import LanguageParser
from project.language.antlr_generated.LanguageVisitor import LanguageVisitor


def get_parse_tree(text: str) -> LanguageParser.ProgramContext:
    """
    Returns the parse tree of a program.
    The `text` parameter should be a string containing the program code.
    """
    return _get_parse_tree(InputStream(text))


def get_parse_tree_from_file(file_name: str) -> LanguageParser.ProgramContext:
    """
    Returns the parse tree of a program read from a file.
    The `file_name` parameter should be the name of the file containing the program code.
    """
    return _get_parse_tree(FileStream(file_name))


def get_parse_tree_from_console() -> LanguageParser.ProgramContext:
    """
    Returns the parse tree of a program read from the console.
    """
    return _get_parse_tree(StdinStream())


def check_syntax(text: str) -> None:
    """
    Check the syntax of a program.
    The `text` parameter should be a string containing the program code.
    """
    get_parse_tree(text)


def to_dot(text: str, file_name: str):
    """
    Generate a graph representation of a program in DOT format.
    The `text` parameter should be a string containing the program code.
    The `file_name` parameter should be a file to save a graph representation.
    """
    vis = _ToDotVisitor()
    tree = get_parse_tree(text)
    tree.accept(vis)
    vis.to_dot(file_name)


def _get_parse_tree(stream: InputStream) -> LanguageParser.ProgramContext:
    class MyErrorListener(ErrorListener):
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            raise ParseCancellationException(f"line {line}:{column} {msg}")

    lexer = LanguageLexer(stream)
    error_listener = MyErrorListener()
    lexer.addErrorListener(error_listener)

    parser = LanguageParser(CommonTokenStream(lexer))
    parser.addErrorListener(error_listener)
    return parser.program()


class _ToDotVisitor(LanguageVisitor):
    def __init__(self):
        self._node_number = 0
        self._graph = MultiDiGraph()

    def to_dot(self, file_name: str):
        nx_agraph.write_dot(self._graph, file_name)

    def next_node_number(self):
        self._node_number += 1
        return self._node_number

    def _get_rule_name(self, rule_number: int):
        return LanguageParser.ruleNames[rule_number]

    def _get_node(self, name: Union[str, int], value=None):
        if isinstance(name, int):
            name = self._get_rule_name(name)
        node_id = f"{name}_{self.next_node_number()}"
        if value != None:
            name += f' ("{value}")'
        self._graph.add_node(node_id, label=name)
        return node_id

    def _add_link(self, par, child, label=None):
        if label != None:
            self._graph.add_edge(par, child, label=label)
        else:
            self._graph.add_edge(par, child)

    def _visit_unary_expr(self, ctx, name: Union[str, int]):
        node = self._get_node(name)
        self._add_link(node, ctx.expr().accept(self))
        return node

    def _visit_binary_expr(
        self,
        ctx,
        name: Union[str, int],
        lhs=None,
        rhs=None,
        lhsLabel="lhs",
        rhsLabel="rhs",
    ):
        node = self._get_node(name)
        if lhs == None:
            lhs = ctx.expr(0)
        if rhs == None:
            rhs = ctx.expr(1)
        self._add_link(node, lhs.accept(self), label=lhsLabel)
        self._add_link(node, rhs.accept(self), label=rhsLabel)
        return node

    def _visit_functor(self, ctx, name: str):
        return self._visit_binary_expr(
            ctx, name, lhs=ctx.with_, rhs=ctx.what, lhsLabel="lambda", rhsLabel="expr"
        )

    def _visit_children(self, ctx, name: Union[str, int], children):
        if isinstance(name, int):
            name = self._get_rule_name(name)
        node = self._get_node(name)
        for pat in children:
            self._add_link(node, pat.accept(self))
        return node

    # Visit a parse tree produced by LanguageParser#program.
    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        return self._visit_children(ctx, LanguageParser.RULE_program, ctx.statement())

    # Visit a parse tree produced by LanguageParser#bind.
    def visitBind(self, ctx: LanguageParser.BindContext):
        return self._visit_binary_expr(
            ctx,
            LanguageParser.RULE_bind,
            lhs=ctx.var(),
            rhs=ctx.expr(),
            lhsLabel="var",
            rhsLabel="expr",
        )

    # Visit a parse tree produced by LanguageParser#print.
    def visitPrint(self, ctx: LanguageParser.PrintContext):
        return self._visit_unary_expr(ctx, LanguageParser.RULE_print)

    # Visit a parse tree produced by LanguageParser#brackets_expr.
    def visitBrackets_expr(self, ctx: LanguageParser.Brackets_exprContext):
        return ctx.expr().accept(self)

    # Visit a parse tree produced by LanguageParser#set_expr.
    def visitSet_start_expr(self, ctx: LanguageParser.Set_start_exprContext):
        return self._visit_binary_expr(
            ctx,
            "set_start_expr",
            lhs=ctx.what,
            rhs=ctx.for_,
            lhsLabel="for",
            rhsLabel="what",
        )

    # Visit a parse tree produced by LanguageParser#set_expr.
    def visitSet_final_expr(self, ctx: LanguageParser.Set_final_exprContext):
        return self._visit_binary_expr(
            ctx,
            "set_final_expr",
            lhs=ctx.what,
            rhs=ctx.for_,
            lhsLabel="for",
            rhsLabel="what",
        )

    # Visit a parse tree produced by LanguageParser#add_start_expr.
    def visitAdd_start_expr(self, ctx: LanguageParser.Add_start_exprContext):
        return self._visit_binary_expr(
            ctx,
            "add_start_expr",
            lhs=ctx.what,
            rhs=ctx.for_,
            lhsLabel="for",
            rhsLabel="what",
        )

    # Visit a parse tree produced by LanguageParser#add_final_expr.
    def visitAdd_final_expr(self, ctx: LanguageParser.Add_final_exprContext):
        return self._visit_binary_expr(
            ctx,
            "add_final_expr",
            lhs=ctx.what,
            rhs=ctx.for_,
            lhsLabel="for",
            rhsLabel="what",
        )

    # Visit a parse tree produced by LanguageParser#start_from_expr.
    def visitStart_from_expr(self, ctx: LanguageParser.Start_from_exprContext):
        return self._visit_unary_expr(ctx, "start_from_expr")

    # Visit a parse tree produced by LanguageParser#final_from_expr.
    def visitFinal_from_expr(self, ctx: LanguageParser.Final_from_exprContext):
        return self._visit_unary_expr(ctx, "final_from_expr")

    # Visit a parse tree produced by LanguageParser#vertexes_from_expr.
    def visitVertexes_from_expr(self, ctx: LanguageParser.Vertexes_from_exprContext):
        return self._visit_unary_expr(ctx, "vertexes_from_expr")

    # Visit a parse tree produced by LanguageParser#edges_from_expr.
    def visitEdges_from_expr(self, ctx: LanguageParser.Edges_from_exprContext):
        return self._visit_unary_expr(ctx, "edges_from_expr")

    # Visit a parse tree produced by LanguageParser#labels_from_expr.
    def visitLabels_from_expr(self, ctx: LanguageParser.Labels_from_exprContext):
        return self._visit_unary_expr(ctx, "labels_from_expr")

    # Visit a parse tree produced by LanguageParser#reach_from_expr.
    def visitReach_from_expr(self, ctx: LanguageParser.Reach_from_exprContext):
        return self._visit_unary_expr(ctx, "reach_from_expr")

    # Visit a parse tree produced by LanguageParser#map_expr.
    def visitMap_expr(self, ctx: LanguageParser.Map_exprContext):
        return self._visit_functor(ctx, "map_expr")

    # Visit a parse tree produced by LanguageParser#filter_expr.
    def visitFilter_expr(self, ctx: LanguageParser.Filter_exprContext):
        return self._visit_functor(ctx, "filter_expr")

    # Visit a parse tree produced by LanguageParser#load_expr.
    def visitLoad_expr(self, ctx: LanguageParser.Load_exprContext):
        return self._visit_unary_expr(ctx, "load_expr")

    # Visit a parse tree produced by LanguageParser#intersect_expr.
    def visitIntersect_expr(self, ctx: LanguageParser.Intersect_exprContext):
        return self._visit_binary_expr(ctx, "intersect_expr")

    # Visit a parse tree produced by LanguageParser#concat_expr.
    def visitConcat_expr(self, ctx: LanguageParser.Concat_exprContext):
        return self._visit_binary_expr(ctx, "concat_expr")

    # Visit a parse tree produced by LanguageParser#union_expr.
    def visitUnion_expr(self, ctx: LanguageParser.Union_exprContext):
        return self._visit_binary_expr(ctx, "union_expr")

    # Visit a parse tree produced by LanguageParser#equal_expr.
    def visitEqual_expr(self, ctx: LanguageParser.Equal_exprContext):
        return self._visit_binary_expr(ctx, "equal_expr")

    # Visit a parse tree produced by LanguageParser#notequal_expr.
    def visitNotequal_expr(self, ctx: LanguageParser.Notequal_exprContext):
        return self._visit_binary_expr(ctx, "notequal_expr")

    # Visit a parse tree produced by LanguageParser#not_expr.
    def visitNot_expr(self, ctx: LanguageParser.Not_exprContext):
        return self._visit_unary_expr(ctx, "not_expr")

    # Visit a parse tree produced by LanguageParser#klein_expr.
    def visitKlein_expr(self, ctx: LanguageParser.Klein_exprContext):
        return self._visit_unary_expr(ctx, "klein_expr")

    # Visit a parse tree produced by LanguageParser#in_set_expr.
    def visitIn_set_expr(self, ctx: LanguageParser.In_set_exprContext):
        return self._visit_binary_expr(
            ctx,
            "in_set_expr",
            lhs=ctx.what,
            rhs=ctx.to,
            lhsLabel="what",
            rhsLabel="where",
        )

    # Visit a parse tree produced by LanguageParser#subset_expr.
    def visitSubset_expr(self, ctx: LanguageParser.Subset_exprContext):
        return self._visit_binary_expr(
            ctx, "subset_expr", lhs=ctx.what, rhs=ctx.of, lhsLabel="what", rhsLabel="of"
        )

    # Visit a parse tree produced by LanguageParser#lambda.
    def visitLambda(self, ctx: LanguageParser.LambdaContext):
        return self._visit_binary_expr(
            ctx,
            "lambda_expr",
            lhs=ctx.patterns(),
            rhs=ctx.expr(),
            lhsLabel="args",
            rhsLabel="body",
        )

    # Visit a parse tree produced by LanguageParser#patterns.
    def visitPatterns(self, ctx: LanguageParser.PatternsContext):
        return self._visit_children(ctx, "patterns", ctx.pattern())

    # Visit a parse tree produced by LanguageParser#tuple_pattern.
    def visitTuple_pattern(self, ctx: LanguageParser.Tuple_patternContext):
        return self._visit_children(ctx, "tuple_pattern", ctx.pattern())

    # Visit a parse tree produced by LanguageParser#var.
    def visitVar(self, ctx: LanguageParser.VarContext):
        return self._get_node("var", str(ctx.ID()))

    # Visit a parse tree produced by LanguageParser#int_val.
    def visitInt_val(self, ctx: LanguageParser.Int_valContext):
        return self._get_node("int_val", str(ctx.INT()))

    # Visit a parse tree produced by LanguageParser#str_val.
    def visitStr_val(self, ctx: LanguageParser.Str_valContext):
        return self._get_node("str_val", str(ctx.STR()))

    # Visit a parse tree produced by LanguageParser#tuple_val.
    def visitTuple_val(self, ctx: LanguageParser.Tuple_valContext):
        return self._visit_children(ctx, "tuple_val", ctx.expr())

    # Visit a parse tree produced by LanguageParser#set_val.
    def visitSet_val(self, ctx: LanguageParser.Set_valContext):
        return self._visit_children(ctx, "set_val", ctx.set_elem())

    # Visit a parse tree produced by LanguageParser#set_elem_interval.
    def visitSet_elem_interval(self, ctx: LanguageParser.Set_elem_intervalContext):
        return self._get_node("set_interval", f"{ctx.INT(0)}..{ctx.INT(1)}")
