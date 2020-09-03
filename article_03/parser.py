from ast import ProgramNode, NumberNode, BinaryOpNode
from lexer import tokenize, InputStream


def parse(tokens):
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos, token
        if not token.type == "EOF":
            pos += 1
            token = tokens[pos]

    def parse_program():
        ast = ProgramNode()
        while not token.type == "EOF":
            ast.children.append(parse_expr())
            get_next_token()
        return ast

    def parse_expr():
        node = parse_term()
        return node

    def parse_term():
        node = parse_factor()
        while token.value in ("+", "-"):
            op = token
            get_next_token()
            node = BinaryOpNode(
                node, op, parse_factor())
        return node

    def parse_factor():
        node = parse_atom()
        if token.type == "NUMBER":
            get_next_token()
        while token.value in ("*", "/"):
            op = token
            get_next_token()
            node = BinaryOpNode(
                node, op, parse_factor())
        return node

    def parse_atom():
        if token.type == "NUMBER":
            return NumberNode(
                token.value)
        if token.value == "(":
            get_next_token()
            node = parse_expr()
            if token.value == ")":
                get_next_token()
            return node

    return parse_program()
