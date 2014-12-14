#!/usr/bin/python
from collections import defaultdict
from SymbolTable import SymbolTable, FunctionSymbol, VariableSymbol
import AST

types_table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    types_table[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    types_table[op]['int']['float'] = 'float'
    types_table[op]['float']['int'] = 'float'
    types_table[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['int']['float'] = 'int'
    types_table[op]['float']['int'] = 'int'
    types_table[op]['float']['float'] = 'int'

types_table['+']['string']['string'] = 'string'
types_table['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    types_table[op]['string']['string'] = 'int'

debug = False


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        if debug:
            print "Visiting class " + node.__class__.__name__ + " (method: " + visitor.__name__ + ")"
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            c = None
            #Some hacking due to wrong attributes' names
            try:
                c = node.children
            except AttributeError:
                try:
                    c = node.declarations
                except AttributeError:
                    try:
                        c = node.instructions
                    except AttributeError:
                        try:
                            c = node.arg_list
                        except AttributeError:
                            try:
                                c = node.fundef_list
                            except AttributeError:
                                try:
                                    c = node.inits
                                except AttributeError:
                                    c = None
            if c is None:
                return
            if type(c) is not list:
                self.visit(c)
            else:
                for child in c:
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
        self.errors = False

    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        t = types_table[op][left][right]
        if t is None:
            self.errors = True
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
            self.errors = True
            print "Undefined symbol {0} in line {1}.".format(node.id, node.lineno)
        else:
            return definition.type

    def visit_Fundef(self, node):
        f = self.table.get(node.id)
        if f:
            self.errors = True
            if type(f) == FunctionSymbol:
                print "Function {0} is already defined at line {1}. Redefinition at line {2}.".format(
                    node.id, f.lineno, node.lineno
                )
            else:
                print "Name {0} is already defined at line {1}. Redefinition at line {2}.".format(
                    node.id, f.lineno, node.lineno
                )
        else:
            f = FunctionSymbol(node.id, node.t, SymbolTable(self.table, node.id), node.lineno)
            self.table.put(node.id, f)
            self.current_func = f
            globalTable = self.table
            self.table = self.current_func.table
            if node.args_list is not None:
                self.visit(node.args_list)
            self.visit(node.comp_instr)
            self.table = globalTable
            self.current_func = None

    def visit_Assignment(self, node):
        pass