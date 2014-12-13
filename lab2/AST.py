class Node(object):
    def __str__(self):
        return self.printTree()


class ID(Node):
    def __init__(self, _id):
        self._id = _id


class Arg(Node):
    def __init__(self, t, idd):
        self.t = t
        self.idd = idd


class ArgList(Node):
    def __init__(self):
        self.arg_list = []

    def append_arg(self, a):
        self.arg_list.append(a)

    def cons_arg(self, arg_list, a):
        self.arg_list = list(arg_list).append(a)


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
        self.fundef_list = list(fundef_list).insert(0, f)


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
        self.expr_list = list(expr_list).append(e)


# class ConstExpr(Node):
#     def __init__(self, constt):
#         self.constt = constt


class IDExpr(Node):
    def __init__(self, _id, leftParen, expr_list_or_err_or_empty, rightParen):
        self._id = _id
        self.leftParen = leftParen
        self.expr_list_or_err_or_empty = expr_list_or_err_or_empty
        self.rightParen = rightParen
        ## if leftParen != rightParen --> throw TerribleSyntaxException


class ParenExpr(Node):
    def __init__(self, expr_or_err):
        self.expression = expr_or_err


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


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
    def __init__(self, var_name, expression):
        self.var_name = var_name
        self.expression = expression


class Instructions(Node):
    def __init__(self):
        self.instructions = []


class LabeledInstruction(Node):
    def __init__(self, label, instr):
        self.label = label
        self.instr = instr


class PrintInstr(Node):
    def __init__(self, to_print):
        self.to_print = to_print


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
    def __init__(self, expr):
        self.expr = expr


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
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr


class Expression(Node):
    pass


class Const(Node):
    def __init__(self, val):
        self.val = val


class Integer(Const):
    def __init__(self, val):
        Const.__init__(self, val)


class Float(Const):
    def __init__(self, val):
        Const.__init__(self, val)


class String(Const):
    def __init__(self, val):
        Const.__init__(self, val)


class Variable(Node):
    def __init__(self, val):
        self.val = val


class Error(Node):
    pass