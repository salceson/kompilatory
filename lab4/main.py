# import sys
# import ply.yacc as yacc
# from Cparser import Cparser
# from TreePrinter import TreePrinter
# from TypeChecker import TypeChecker
#
# semantic_control = True
# print_tree = False
#
# if __name__ == '__main__':
#     TreePrinter()  # Loads printTree definitions
#
#     try:
#         filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
#         file = open(filename, "r")
#     except IOError:
#         print("Cannot open {0} file".format(filename))
#         sys.exit(0)
#
#     c_parser = Cparser()
#     parser = yacc.yacc(module=c_parser)
#     text = file.read()
#
#     ast = parser.parse(text, lexer=c_parser.scanner)
#
#     if c_parser.errors:
#         print "There were errors in your code. Please correct them."
#         exit(1)
#
#     if print_tree:
#         print "Parsing tree:\n"
#         str = ast.printTree()
#         print str
#
#     if semantic_control:
#         print "Starting semantic control..."
#
#         typeChecker = TypeChecker()
#         typeChecker.visit(ast)
#
#         print "Done"
#
#         if typeChecker.errors:
#             print "There were errors in your code. Please correct them."
#             exit(1)


import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    parser.parse(text, lexer=Cparser.scanner)

    ast = parser.parse(text, lexer=Cparser.scanner)
    ast.accept(TypeChecker())

    # jesli wizytor TypeChecker z implementacji w poprzednim lab korzystal z funkcji accept
    # to nazwa tej ostatniej dla Interpretera powinna zostac zmieniona, np. na accept2 ( ast.accept2(Interpreter()) )
    # tak aby rozne funkcje accept z roznych implementacji wizytorow nie kolidowaly ze soba
    ast.accept(Interpreter())

    # in future
    # ast.accept(OptimizationPass1())
    # ast.accept(OptimizationPass2())
    # ast.accept(CodeGenerator())
