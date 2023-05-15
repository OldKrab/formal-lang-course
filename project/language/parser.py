from antlr4 import (
    CommonTokenStream,
    InputStream,
    FileStream,
    StdinStream,
)
from antlr4.error.Errors import ParseCancellationException
from antlr4.error.ErrorListener import ErrorListener
from networkx import MultiDiGraph
from networkx.drawing import nx_pydot
from project.language.antlr_generated.LanguageLexer import LanguageLexer
from project.language.antlr_generated.LanguageParser import LanguageParser
from project.language.antlr_generated.LanguageVisitor import LanguageVisitor


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


def get_parse_tree(text: str) -> LanguageParser.ProgramContext:
    return _get_parse_tree(InputStream(text))


def get_parse_tree_from_file(file_name: str) -> LanguageParser.ProgramContext:
    return _get_parse_tree(FileStream(file_name))


def get_parse_tree_from_console() -> LanguageParser.ProgramContext:
    return _get_parse_tree(StdinStream())


def check_syntax(text: str) -> None:
    get_parse_tree(text)


class _ToDotVisitor(LanguageVisitor):
    def __init__(self):
        self._node_number = 0
        self._graph = MultiDiGraph()

    def to_dot(self):
        nx_pydot.write_dot(self._graph, "temp")

    def next_node_number(self):
        self._node_number += 1
        return self._node_number

    def _get_node_name(self, name: str):
        return f"{name}_{self.next_node_number()}"

    def _get_rule_node_name(self, rule_number: int):
        return self._get_node_name(LanguageParser.ruleNames[rule_number])

    def _add_link(self, par, child):
        self._graph.add_edge(par, child)

        # Visit a parse tree produced by LanguageParser#program.

    def visitProgram(self, ctx: LanguageParser.ProgramContext):
        node = self._get_rule_node_name(LanguageParser.RULE_program)
        for stat in ctx.statements:
            child = stat.accept(self)
            self._graph.add_edge(node, child)
        return node

    # Visit a parse tree produced by LanguageParser#bind.
    def visitBind(self, ctx: LanguageParser.BindContext):
        node = self._get_rule_node_name(LanguageParser.RULE_bind)
        self._add_link(node, ctx.var().accept(self))
        self._add_link(node, ctx.expr().accept(self))
        return node

    # Visit a parse tree produced by LanguageParser#print.
    def visitPrint(self, ctx: LanguageParser.PrintContext):
        node = self._get_rule_node_name(LanguageParser.RULE_print)
        self._add_link(node, ctx.expr().accept(self))
        return node

    # Visit a parse tree produced by LanguageParser#in_set_expr.
    def visitIn_set_expr(self, ctx: LanguageParser.In_set_exprContext):
        node = self._get_node_name("set_expr")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#edges_from_expr.
    def visitEdges_from_expr(self, ctx: LanguageParser.Edges_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#notequal_expr.
    def visitNotequal_expr(self, ctx: LanguageParser.Notequal_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#not_expr.
    def visitNot_expr(self, ctx: LanguageParser.Not_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#vertexes_from_expr.
    def visitVertexes_from_expr(self, ctx: LanguageParser.Vertexes_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#brackets_expr.

    def visitBrackets_expr(self, ctx: LanguageParser.Brackets_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#labels_from_expr.
    def visitLabels_from_expr(self, ctx: LanguageParser.Labels_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#map_expr.
    def visitMap_expr(self, ctx: LanguageParser.Map_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#reach_from_expr.
    def visitReach_from_expr(self, ctx: LanguageParser.Reach_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#concat_expr.
    def visitConcat_expr(self, ctx: LanguageParser.Concat_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#klein_expr.
    def visitKlein_expr(self, ctx: LanguageParser.Klein_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#load_expr.
    def visitLoad_expr(self, ctx: LanguageParser.Load_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#union_expr.
    def visitUnion_expr(self, ctx: LanguageParser.Union_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#final_from_expr.
    def visitFinal_from_expr(self, ctx: LanguageParser.Final_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#lambda_expr.
    def visitLambda_expr(self, ctx: LanguageParser.Lambda_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#subset_expr.
    def visitSubset_expr(self, ctx: LanguageParser.Subset_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#equal_expr.
    def visitEqual_expr(self, ctx: LanguageParser.Equal_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#set_expr.
    def visitSet_expr(self, ctx: LanguageParser.Set_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#val_expr.
    def visitVal_expr(self, ctx: LanguageParser.Val_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#filter_expr.
    def visitFilter_expr(self, ctx: LanguageParser.Filter_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#start_from_expr.
    def visitStart_from_expr(self, ctx: LanguageParser.Start_from_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#var_expr.
    def visitVar_expr(self, ctx: LanguageParser.Var_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#intersect_expr.
    def visitIntersect_expr(self, ctx: LanguageParser.Intersect_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#add_start_expr.
    def visitAdd_start_expr(self, ctx: LanguageParser.Add_start_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#add_final_expr.
    def visitAdd_final_expr(self, ctx: LanguageParser.Add_final_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#lambda.
    def visitLambda(self, ctx: LanguageParser.LambdaContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#patterns.
    def visitPatterns(self, ctx: LanguageParser.PatternsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#pattern.
    def visitPattern(self, ctx: LanguageParser.PatternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#tuple_pattern.
    def visitTuple_pattern(self, ctx: LanguageParser.Tuple_patternContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#var.
    def visitVar(self, ctx: LanguageParser.VarContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#val.
    def visitVal(self, ctx: LanguageParser.ValContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#simple_val.
    def visitSimple_val(self, ctx: LanguageParser.Simple_valContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#tuple_val.
    def visitTuple_val(self, ctx: LanguageParser.Tuple_valContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#set_val.
    def visitSet_val(self, ctx: LanguageParser.Set_valContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#set_elem.
    def visitSet_elem(self, ctx: LanguageParser.Set_elemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LanguageParser#set_elem_interval.
    def visitSet_elem_interval(self, ctx: LanguageParser.Set_elem_intervalContext):
        return self.visitChildren(ctx)


def to_dot(text: str):
    vis = _ToDotVisitor()
    tree = get_parse_tree(text)
    tree.accept(vis)
    vis.to_dot()
