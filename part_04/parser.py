from ast import ProgramNode, NumberNode, BinaryOpNode, UnaryOpNode, IdentifierNode, CallExpressionNode


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
        if token.type == "NUMBER" or token.type == "OPERATOR":
            return parse_term()
        if token.value == "(":
            return parse_term()
        if token.type == "IDENTIFIER":
            return maybe_call()

    def parse_call(name_token):
        args = []
        get_next_token()
        while token.value != ")":
            if token.value == ",":
                get_next_token()
            args.append(parse_expr())
        # Skip closing paren
        get_next_token()
        return CallExpressionNode(name_token.value, args)

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
        if token.type == "OPERATOR":
            op = token
            get_next_token()
            return UnaryOpNode(op, parse_atom())
        if token.type == "NUMBER":
            return NumberNode(
                token.value)
        if token.value == "(":
            get_next_token()
            print(token)
            node = parse_expr()
            if token.value == ")":
                get_next_token()
            return node
        if token.type == "IDENTIFIER":
            return IdentifierNode(token.value)

    def maybe_call():
        name_token = token
        next = lookahead()
        if next.value == "(":
            get_next_token()
            return parse_call(name_token)
        return parse_atom()

    return parse_program()
