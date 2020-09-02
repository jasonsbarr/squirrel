from lexer import InputStream, lexer
from parser import parse
from interpreter import evaluate


def repl():
    while True:
        try:
            program = input("squirrel> ")
        except EOFError:
            print("")
            print("Goodbye!")
            break
        if not program:
            continue

        print(evaluate(parse(lexer(InputStream(program)))))


if __name__ == "__main__":
    repl()
