from ast import ProgramNode, NumberNode


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
            ast.children.append(NumberNode(
                token.value, {
                    "line": token.line, "col": token.start}, {
                    "line": token.line, "col": token.end}))

        token = get_next_token()

    return ast
