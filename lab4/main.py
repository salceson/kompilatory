import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter
from TreePrinter import TreePrinter

print_tree = False

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)


    cparser = Cparser()
    parser = yacc.yacc(module=cparser)
    text = file.read()
    ast = parser.parse(text, lexer=cparser.scanner)
    print "Parsing file..."
    if cparser.errors:
        print "There were errors while parsing file {0}.".format(filename)
        print "Please correct them."
        exit(1)

    if print_tree:
        tp = TreePrinter()
        print "Parsing tree:"
        print ast.printTree()

    print "Performing semantic control..."
    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    if typeChecker.errors:
        print "There were errors while performing semantic control in file {0}.".format(filename)
        print "Please correct them."
        exit(2)

    print "Interpreting..."
    ast.accept(Interpreter())