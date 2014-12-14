#!/usr/bin/python
from collections import defaultdict
from SymbolTable import SymbolTable
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
        if ttype[op][left][right] is None:
            print "Bad expression {0} in line {1}".format(op, node.lineno)
        return ttype[op][left][right]

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node._id)
        if definition is None:
            print "Undefined symbol {0} in line {1}.".format(node._id, node.lineno)
        else:
            return definition.type

    def visit_Funcall(self, node):
        pass
