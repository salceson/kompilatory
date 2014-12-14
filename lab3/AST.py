class Node(object):
    def __str__(self):
        return self.printTree()


class Arg(Node):
    def __init__(self, t, idd, lineno):
        self.t = t
        self.idd = idd
        self.lineno = lineno


class ArgList(Node):
    def __init__(self):
        self.arg_list = []
        self.children = self.arg_list

    def append_arg(self, a):
        self.arg_list.append(a)

    def cons_arg(self, arg_list, a):
        self.arg_list = list(arg_list)
        self.arg_list.append(a)


class Fundef(Node):
    def __init__(self, t, _id, args_list, comp_instr):
        self.t = t
        self._id = _id
        self.args_list = args_list
        self.comp_instr = comp_instr


class FundefList(Node):
    def __init__(self):
        self.fundef_list = []

    def append_fun(self, f):
        self.fundef_list.append(f)

    def cons_fun(self, fundef_list, f):
        self.fundef_list = list(fundef_list)
        self.fundef_list.insert(0, f)


# mozna sie klocic, czy to jest potrzebne, ale przyjalem zasade
# jest produkcja --> jest klasa. Nie trzeba sie zastanawiac i robic logiki
# dzieki temu
class Empty(Node):
    def __init__(self):
        pass


class ExprList(Node):
    def __init__(self):
        self.expr_list = []

    def append_expr(self, e):
        self.expr_list.append(e)

    def cons_expr(self, expr_list, e):      # ta metoda to nie wiem, ale niech juz bedzie
        self.expr_list = list(expr_list)
        self.expr_list.append(e)


class Expression(Node):
    pass


class Funcall(Expression):
    def __init__(self, _id, expr_list, lineno):
        self._id = _id
        self.expr_list = expr_list
        self.lineno = lineno


class Variable(Expression):
    def __init__(self, _id, lineno):
        self._id = _id
        self.lineno = lineno


class ParenExpr(Expression):
    def __init__(self, expr_or_err):
        self.expression = expr_or_err


class BinExpr(Expression):
    def __init__(self, op, left, right, lineno):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno


class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions


class Declarations(Node):
    def __init__(self):
        self.declarations = []


class Declaration(Node):
    def __init__(self, declaration_type, inits):
        self.declaration_type = declaration_type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.inits = []


class Init(Node):
    def __init__(self, var_name, expression, lineno):
        self.var_name = var_name
        self.expression = expression
        self.lineno = lineno


# Instructions
class Instructions(Node):
    def __init__(self):
        self.instructions = []


class LabeledInstruction(Node):
    def __init__(self, label, instr, lineno):
        self.label = label
        self.instr = instr
        self.lineno = lineno


class PrintInstr(Node):
    def __init__(self, to_print, lineno):
        self.to_print = to_print
        self.lineno = lineno


class IfInstr(Node):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class IfElseInstr(Node):
    def __init__(self, cond, instr, else_instr):
        self.cond = cond
        self.instr = instr
        self.elseinstr = else_instr


class WhileInstr(Node):
    def __init__(self, cond, instr):
        self.cond = cond
        self.instr = instr


class RepeatInstr(Node):
    def __init__(self, cond, instrs):
        self.cond = cond
        self.instrs = instrs


class ReturnInstr(Node):
    def __init__(self, expr, lineno):
        self.expr = expr
        self.lineno = lineno


class ContinueInstr(Node):
    def __init__(self):
        pass


class BreakInstr(Node):
    def __init__(self):
        pass


class CompoundInstr(Node):
    def __init__(self, decls, instrs):
        self.decls = decls
        self.instrs = instrs


class Assignment(Node):
    def __init__(self, var, expr, lineno):
        self.var = var
        self.expr = expr
        self.lineno = lineno


# Constants
class Const(Node):
    def __init__(self, val, lineno):
        self.val = val
        self.lineno = lineno


class Integer(Const):
    def __init__(self, val, lineno):
        Const.__init__(self, val, lineno)


class Float(Const):
    def __init__(self, val, lineno):
        Const.__init__(self, val, lineno)


class String(Const):
    def __init__(self, val, lineno):
        Const.__init__(self, val, lineno)


class Error(Node):
    pass