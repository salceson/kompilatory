import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *


class Interpreter(object):
    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        l = node.left.accept(self)
        r = node.right.accept(self)
        op = node.op
        return eval("a" + op + "b", {"a": l, "b": r})

    @when(AST.ParenExpr)
    def visit(self, node):
        return node.expression.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.WhileInstr)
    def visit(self, node):
        while node.cond.accept(self):
            try:
                node.instr.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break

    @when(AST.RepeatInstr)
    def visit(self, node):
        while True:
            try:
                node.instrs.accept(self)
                if node.cond.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.IfInstr)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)

    @when(AST.IfElseInstr)
    def visit(self, node):
        if node.cond.accept(self):
            return node.instr.accept(self)
        else:
            return node.elseinstr.accept(self)

    @when(AST.ExprList)
    def visit(self, node):
        for expr in node.expr_list:
            expr.accept(self)

    @when(AST.Instructions)
    def visit(self, node):
        for instr in node.instructions:
            instr.accept(self)