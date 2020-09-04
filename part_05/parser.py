from ast import ProgramNode, NumberNode, BinaryOpNode, UnaryOpNode, IdentifierNode, CallExpressionNode
from lexer import InputStream, tokenize


PRECEDENCE = {
    "=": 1,
    "+": 8, "-": 8,
    "*": 10, "/": 10
}


def parse(tokens):
    pos = 0
    token = tokens[pos]

    def get_next_token():
        nonlocal pos, token
        if not token.type == "EOF":
            pos += 1
            token = tokens[pos]

    def lookahead():
        if not token.type == "EOF":
            return tokens[pos + 1]
        else:
            return token

    def parse_program():
        ast = ProgramNode()
        while not token.type == "EOF":
            ast.children.append(parse_expr())
            get_next_token()
        return ast

    def parse_expr():
        # Expression is term
        if token.type == "NUMBER":
            return maybe_binary(parse_atom(), 0)
        if token.type == "OPERATOR":
            return parse_atom()
        if token.type == "IDENTIFIER":
            return maybe_call()

    def parse_call(name_token):
        args = []
        # Skip opening paren
        get_next_token()
        while token.value != ")":
            if token.value == ",":
                get_next_token()
            args.append(parse_expr())
        # Skip closing paren
        get_next_token()
        return CallExpressionNode(name_token.value, args)

    def parse_atom():
        if token.type == "OPERATOR":
            op = token
            get_next_token()
            return UnaryOpNode(op, parse_atom())
        if token.type == "NUMBER":
            return NumberNode(
                token.value)
        if token.value == "(":
            get_next_token()
            node = parse_expr()
            if token.value == ")":
                get_next_token()
            return node
        if token.type == "IDENTIFIER":
            return IdentifierNode(token.value)

    def maybe_binary(left, my_prec=0):
        next = lookahead()
        if next.type == "OPERATOR":
            get_next_token()
            precedence = PRECEDENCE[token.value]
            if precedence > my_prec:
                get_next_token()
                right = maybe_binary(parse_atom(), precedence)
                binary = BinaryOpNode(
                    "AssignmentOperation" if next.value == "=" else "BinaryOperation",
                    left,
                    next,
                    right)
                return maybe_binary(binary, my_prec)
        return left

    def maybe_call():
        name_token = token
        next = lookahead()
        if next.value == "(":
            get_next_token()
            return parse_call(name_token)
        return maybe_binary(parse_atom(), 0)

    return parse_program()
