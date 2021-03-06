import sys
import ply.yacc as yacc
from Cparser import Cparser
from TreePrinter import TreePrinter


if __name__ == '__main__':
    TreePrinter()  # Loads printTree definitions

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    program = parser.parse(text, lexer=Cparser.scanner)
    str = program.printTree()
    print str

