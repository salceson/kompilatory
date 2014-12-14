#!/usr/bin/python
from collections import defaultdict
from SymbolTable import SymbolTable, FunctionSymbol
import AST

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            try:
                c = node.children
            except AttributeError:
                return
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.current_type = ""
        self.current_func = None

    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        t = ttype[op][left][right]
        if t is None:
            print "Cannot perform operation {0} between types {1} and {2} at line {3}".format(
                op, left, right, node.lineno
            )
        return t

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node.id)
        if definition is None:
            print "Undefined symbol {0} in line {1}.".format(node.id, node.lineno)
        else:
            return definition.type

    def visit_Funcall(self, node):
        f = self.table.get(node.id)
        if f:
            if type(f) == FunctionSymbol:
                print "Function {0} is already defined at line {1}. Redefinition at line {2}.".format(
                    node.id, f.lineno, node.lineno
                )
            else:
                print "Redefinition of name {0} (previously defined at line {1}). Redefinition at line {2}.".format(
                    node.id, f.lineno, node.lineno
                )
        else:
            f = FunctionSymbol(node.id, node.t, SymbolTable(self.table, node.id), node.lineno)
            self.table.put(node.id, f)
            self.current_func = node.id
            globalTable = self.table
            self.table = self.current_func.table
            if node.args_list is not None:
                self.visit(node.args_list)
            self.visit(node.comp_instr)
            self.table = globalTable
            self.current_func = None

    def visit_Assignment(self, node):
        pass