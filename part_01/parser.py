from ast import ProgramNode, NumberNode


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
                token.value)

    return parse_program()
