import sys

from lexer import tokenize, InputStream
from parser import parse
from interpreter import evaluate


code = sys.argv[1]
program = open(code).read()


print(evaluate(parse(tokenize(InputStream(program)))))
