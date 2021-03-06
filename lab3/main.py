import sys
import ply.yacc as yacc
from Cparser import Cparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

semantic_control = True
print_tree = False

if __name__ == '__main__':
    TreePrinter()  # Loads printTree definitions

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    c_parser = Cparser()
    parser = yacc.yacc(module=c_parser)
    text = file.read()

    ast = parser.parse(text, lexer=c_parser.scanner)

    if c_parser.errors:
        print "There were errors in your code. Please correct them."
        exit(1)

    if print_tree:
        print "Parsing tree:\n"
        str = ast.printTree()
        print str

    if semantic_control:
        print "Starting semantic control..."

        typeChecker = TypeChecker()
        typeChecker.visit(ast)

        print "Done"

        if typeChecker.errors:
            print "There were errors in your code. Please correct them."
            exit(1)