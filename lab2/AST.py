class Node(object):
    def __str__(self):
        return self.printTree()


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
    pass


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    pass


class Error(Node):
    pass