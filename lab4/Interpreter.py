import string
import AST
from Memory import *
from Exceptions import *
from visit import *


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node, create_memory=True):
        pass

    @when(AST.BinExpr)
    def visit(self, node, create_memory=True):
        l = node.left.accept(self)
        r = node.right.accept(self)
        op = node.op
        return eval("a" + op + "b", {"a": l, "b": r})

    @when(AST.ParenExpr)
    def visit(self, node, create_memory=True):
        return node.expression.accept(self)

    @when(AST.WhileInstr)
    def visit(self, node, create_memory=True):
        while node.cond.accept(self):
            try:
                node.instr.accept(self)
            except ContinueException:
                pass
            except BreakException:
                break

    @when(AST.RepeatInstr)
    def visit(self, node, create_memory=True):
        while True:
            try:
                node.instrs.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
            if node.cond.accept(self):
                break

    @when(AST.IfInstr)
    def visit(self, node, create_memory=True):
        if node.cond.accept(self):
            return node.instr.accept(self)

    @when(AST.IfElseInstr)
    def visit(self, node, create_memory=True):
        if node.cond.accept(self):
            return node.instr.accept(self)
        else:
            return node.elseinstr.accept(self)

    @when(AST.ExprList)
    def visit(self, node, create_memory=True):
        for expr in node.expr_list:
            expr.accept(self)

    @when(AST.Instructions)
    def visit(self, node, create_memory=True):
        for instr in node.instructions:
            instr.accept(self)

    @when(AST.CompoundInstr)
    def visit(self, node, create_memory=True):
        if create_memory:
            self.memory_stack.push(Memory("inner"))
        node.decls.accept(self)
        try:
            node.instrs.accept(self)
        finally:
            if create_memory:
                self.memory_stack.pop()

    @when(AST.Fundef)
    def visit(self, node, create_memory=True):
        self.memory_stack.peek().put(node.id, node)

    @when(AST.Funcall)
    def visit(self, node, create_memory=True):
        fun = self.memory_stack.get(node.id)
        fun_memory = Memory(node.id)
        if node.expr_list is not None:
            for arg_expression, actual_arg in zip(node.expr_list.expr_list, fun.args_list.arg_list):
                arg = actual_arg.accept(self)
                expr = arg_expression.accept(self)
                fun_memory.put(arg, expr)
        self.memory_stack.push(fun_memory)
        try:
            fun.comp_instr.accept(self, False)
        except ReturnValueException as e:
            return e.value
        finally:
            self.memory_stack.pop()

    @when(AST.Arg)
    def visit(self, node, create_memory=True):
        return node.idd

    @when(AST.ArgList)
    def visit(self, node, create_memory=True):
        for arg in node.arg_list:
            arg.accept(self)

    @when(AST.Assignment)
    def visit(self, node, create_memory=True):
        expr = node.expr.accept(self)
        self.memory_stack.set(node.var, expr)
        return expr

    @when(AST.BreakInstr)
    def visit(self, node, create_memory=True):
        raise BreakException()

    @when(AST.ContinueInstr)
    def visit(self, node, create_memory=True):
        raise ContinueException()

    @when(AST.Declaration)
    def visit(self, node, create_memory=True):
        node.inits.accept(self)

    @when(AST.Declarations)
    def visit(self, node, create_memory=True):
        for declaration in node.declarations:
            declaration.accept(self)

    @when(AST.Init)
    def visit(self, node, create_memory=True):
        expr = node.expression.accept(self)
        self.memory_stack.peek().put(node.var_name, expr)
        return expr

    @when(AST.Inits)
    def visit(self, node, create_memory=True):
        for init in node.inits:
            init.accept(self)

    @when(AST.LabeledInstruction)
    def visit(self, node, create_memory=True):
        return node.instr.accept(self)

    @when(AST.Integer)
    def visit(self, node, create_memory=True):
        return int(node.val)

    @when(AST.Float)
    def visit(self, node, create_memory=True):
        return float(node.val)

    @when(AST.String)
    def visit(self, node, create_memory=True):
        return node.val

    @when(AST.PrintInstr)
    def visit(self, node, create_memory=True):
        to_print = str(node.to_print.accept(self))
        while to_print[0] == '"' and to_print[-1] == '"':
            to_print = string.replace(string.replace(to_print, r'"', "", 1), r'"', "", -1)
        print to_print

    @when(AST.ReturnInstr)
    def visit(self, node, create_memory=True):
        raise ReturnValueException(node.expr.accept(self))

    @when(AST.Variable)
    def visit(self, node, create_memory=True):
        return self.memory_stack.get(node.id)

    @when(AST.FundefList)
    def visit(self, node, create_memory=True):
        for fundef in node.fundef_list:
            fundef.accept(self)

    @when(AST.Program)
    def visit(self, node, create_memory=True):
        node.declarations.accept(self)
        node.fundefs.accept(self)
        node.instructions.accept(self)