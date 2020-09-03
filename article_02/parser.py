from ast import ProgramNode, Point, NumberNode


def parse(tokens):
    ast = ProgramNode(tokens)
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos
        pos += 1
        return tokens[pos]

    def parse_atom():
        if token.type == "NUMBER":
            return NumberNode(
                token.value, Point(
                    token.line, token.start), Point(
                    token.line, token.end))

    while not token.type == "EOF":
        ast.children.append(parse_atom())

        token = get_next_token()

    return ast