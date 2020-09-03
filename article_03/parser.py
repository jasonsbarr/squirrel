from ast import ProgramNode, Point, NumberNode, BinaryOpNode


def parse(tokens):
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos
        pos += 1
        return tokens[pos]

    def parse_program():
        nonlocal token
        ast = ProgramNode(tokens)
        while not token.type == "EOF":
            ast.children.append(parse_atom())
            token = get_next_token()
        return ast

    def parse_atom():
        if token.type == "NUMBER":
            return NumberNode(
                token.value, Point(
                    token.line, token.start), Point(
                    token.line, token.end))

    return parse_program()
