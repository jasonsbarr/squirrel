from article_01.ast import ProgramNode, NumberNode


def parser(tokens):
    ast = ProgramNode(tokens)
    pos = -1

    def get_next_token():
        nonlocal pos
        pos += 1
        return tokens[pos]

    while not current.type == "EOF":
        token = get_next_token()

        if token.type == "NUMBER":
            ast.children.append(NumberNode(
                token.value, {
                    "line": token.line, "col": token.start}, {
                    "line": token.line, "col": token.end}))
