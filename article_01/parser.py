from ast import ProgramNode, NumberNode


class Point:

    def __init__(self, line, col):
        self.line = line
        self.col = col

    def __str__(self):
        return f"({self.line}:{self.col})"

    def __repr__(self):
        return f"Point({self.line}, {self.col})"


def parse(tokens):
    ast = ProgramNode(tokens)
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos
        pos += 1
        return tokens[pos]

    while not token.type == "EOF":
        if token.type == "NUMBER":
            ast.children.append(
                NumberNode(
                    token.value, Point(
                        token.line, token.col), Point(
                        token.line, token.col)))

        token = get_next_token()

    return ast
