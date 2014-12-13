import AST

indent_char = '| '


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


### konwencja jest taka, ze to kazdy Node powinien zrobic nowa linie
### przy wypisywaniu sie (parent nie musi sie o to troszczyc)
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

    @addToClass(AST.Arg)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += "Arg " + self.idd + '\n'
        return res

    @addToClass(AST.ArgList)
    def printTree(self, indent=0):
        res = ""
        for argg in self.arg_list:
            res += argg.printTree(indent + 1)
        return res

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        res = indent * indent_char + "=\n"
        res += self.var.printTree(indent + 1)
        res += self.expr.printTree(indent + 1)
        return res

    @addToClass(AST.BreakInstr)
    def printTree(self, indent=0):
        return indent * indent_char + " BREAK\n"


    @addToClass(AST.Const)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.val + "\n"
        return res

    @addToClass(AST.Integer)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += "int " + self.val + "\n"
        return res

    @addToClass(AST.Float)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += "float " + self.val + "\n"
        return res

    @addToClass(AST.String)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += "string " + self.val + "\n"
        return res

    @addToClass(AST.ID)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.val + "\n"
        return res

    @addToClass(AST.CompoundInstr)
    def printTree(self, indent=0):
        res = ""
        res += self.decls.printTree(indent)
        res += self.instrs.printTree(indent)
        return res

    @addToClass(AST.ContinueInstr)
    def printTree(self, indent=0):
        return indent * indent_char + " CONTINUE\n"


    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        res = indent * indent_char + "DECL\n"
        res += self.inits.printTree(indent + 1)
        return res

    @addToClass(AST.Declarations)
    def printTree(self, indent=0):
        res = ""
        for d in self.declarations:
            res += d.printTree(indent)
        return res

    @addToClass(AST.Init)
    def printTree(self, indent=0):
        res = indent * indent_char + "=\n"
        res += (indent + 1) * indent_char + self.var_name
        res += self.expression.printTree(indent + 1)
        return res

    @addToClass(AST.Inits)
    def printTree(self, indent=0):
        res = ""
        for i in self.inits:
            res += i.printTree(indent)
        return res

    @addToClass(AST.Empty)
    def printTree(self, indent=0):
        return ""

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        return "ERROR"    # TODO errory trzeba oblsugiwac i wtedy wypisywac

    # TODO AST.Expression

    @addToClass(AST.ExprList)
    def printTree(self, indent=0):
        res = ""
        for e in self.expr_list:
            res += e.printTree(indent)
        return res

    @addToClass(AST.IDExpr)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self._id + '\n'
        res += self.expr_list_or_err_or_empty.printTree(indent + 1)
        return res

    @addToClass(AST.IfInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        return res

    @addToClass(AST.IfElseInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        res += indent * indent_char + "ELSE\n"
        res += self.elseintr.printTree(indent + 1)
        return res

    @addToClass(AST.WhileInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "WHILE\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        return res

    @addToClass(AST.RepeatInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "REPEAT\n"
        res += self.cond.printTree(indent + 1)
        res += self.instrs.printTree(indent + 1)
        return res

    @addToClass(AST.ReturnInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "RETURN\n"
        res += self.expr.printTree(indent + 1)
        return res

    @addToClass(AST.PrintInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "PRINT\n"
        res += self.to_print.printTree(indent + 1)
        return res

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent=0):
        res = self.label.printTree(indent)
        res += self.instr.printTree(indent + 1)
        return res

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        res = ""
        for i in self.instructions:
            res += i.printTree(indent)
        return res

    @addToClass(AST.ParenExpr)
    def printTree(self, indent=0):
        # nie wypisujemy nawiasow w ASt, wiec w sumie to samo, co zwykle expression
        return self.expr_or_err.printTree(indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        # jak wyzej, typ nam niepotrzebny w AST, wypisujemy jak zwykle expression
        return self.val.printTree(indent)

    @addToClass(AST.Fundef)
    def printTree(self, indent=0):
        res = indent * indent_char + "FUNDEF\n"
        res += (indent + 1) * indent_char + self._id
        res += (indent + 1) * indent_char + "RET " + self.t
        res += self.args_list.printTree(indent + 1)
        res += self.comp_instr.printTree(indent + 1)
        return res

    @addToClass(AST.FundefList)
    def printTree(self, indent=0):
        res = ""
        print type(self)
        print self.fundef_list
        for f in self.fundef_list:
            res += f.printTree(indent)
        return res
