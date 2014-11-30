import AST

indent_char = '|'


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        res = indent_char * indent
        res += self.op + '\n'
        res += self.left.printTree(indent + 1)
        res += self.right.printTree(indent + 1)
        return res

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        res = ""
        res += self.declarations.printTree(indent + 1)
        res += self.fundefs.printTree(indent + 1)
        res += self.instructions.printTree(indent + 1)
        return res
