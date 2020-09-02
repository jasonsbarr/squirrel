from article_01.ast import ProgramNode, NumberNode


def parse(tokens):
    ast = ProgramNode(tokens)
    pos = -1
    token = None

    def get_next_token():
        nonlocal pos
        pos += 1
        return tokens[pos]

    while not token.type == "EOF":
        token = get_next_token()

        if token.type == "NUMBER":
            ast.children.append(NumberNode(
                token.value, {
                    "line": token.line, "col": token.start}, {
                    "line": token.line, "col": token.end}))
