from lexer import InputStream, InputException, lexer
from parser import parse
from interpreter import evaluate


def repl():
    while True:
        program = ""
        try:
            program = input("squirrel> ")
        except EOFError:
            print("")
            print("Goodbye!")
            break
        if not program:
            continue

        try:
            print(evaluate(parse(lexer(InputStream(program)))))
        except InputException as e:
            print(e)


if __name__ == "__main__":
    repl()
