from ast import ProgramNode, Point, NumberNode, BinaryOpNode


def parse(tokens):
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos, token
        pos += 1
        token = tokens[pos]

    def parse_program():
        ast = ProgramNode(tokens)
        while not token.type == "EOF":
            ast.children.append(parse_expr())
            get_next_token()
        return ast

    def parse_expr():
        return parse_term()

    def parse_term():
        return parse_factor()

    def parse_factor():
        return parse_atom()

    def parse_atom():
        if token.type == "NUMBER":
            return NumberNode(
                token.value, Point(
                    token.line, token.start), Point(
                    token.line, token.end))

    return parse_program()
