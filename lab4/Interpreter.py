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

    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.WhileInstr)
    def visit(self, node):
        r = None
        while node.cond.accept(self):
            r = node.body.accept(self)
        return r